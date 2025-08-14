#include <sys/param.h>

#include <sys/types.h>

#include <sys/proc.h>
#include <sys/systm.h>
#include <sys/syscall.h>
#include <sys/mutex.h>
#include <sys/errno.h>

/* These are required for sys/syscallargs.h */
#include <sys/socket.h>
#include <sys/mount.h>

#include <sys/syscallargs.h>

#include <sys/sendnum.h>

#include <uvm/uvm.h>
#include <uvm/uvm_param.h>
#include <uvm/uvm_addr.h>

enum sendnum_flags {
	SEND_WAITING	= (1<<0),
	RECV_WAITING	= (1<<1),
	TRANSFER_DONE	= (1<<2),
};

static struct mutex sendnum_mtx = MUTEX_INITIALIZER(IPL_NONE);
static uint32_t sendnum_flags = 0;
static vaddr_t sendnum_saddr;
static vaddr_t sendnum_daddr;
static size_t sendnum_len;
static struct proc *sendnum_sender = NULL;
static struct proc *sendnum_receiver = NULL;

static int
sendnum_finish(void)
{
	struct vm_map *dmap, *smap;
	vaddr_t daddr, saddr;
	int eno;
	size_t len;
	struct uvm_map_deadq dead;

	MUTEX_ASSERT_LOCKED(&sendnum_mtx);

	if (!(sendnum_flags & SEND_WAITING))
		return (EAGAIN);
	if (!(sendnum_flags & RECV_WAITING))
		return (EAGAIN);

	KASSERT(!(sendnum_flags & TRANSFER_DONE));
	KASSERT(sendnum_sender != NULL);
	KASSERT(sendnum_receiver != NULL);

	smap = &sendnum_sender->p_vmspace->vm_map;
	dmap = &sendnum_receiver->p_vmspace->vm_map;

	len = sendnum_len;
	saddr = sendnum_saddr;

	/* Round len up to a whole page. */
	len = round_page(len);

again:
	/* First, work out what destination address to put it at. */
	daddr = uvm_map_hint(sendnum_receiver->p_vmspace, PROT_READ,
	    VM_MIN_ADDRESS, VM_MAXUSER_ADDRESS);
	eno = uvm_map_mquery(dmap, &daddr, len, UVM_UNKNOWN_OFFSET, 0);
	if (eno)
		return (eno);

	/* Now we copy the mapping. */
	eno = uvm_share(dmap, daddr, PROT_READ, smap, saddr, len);
	/* We get ENOMEM if the daddr is not available */
	if (eno == ENOMEM)
		goto again;

	/* And delete the original one. */
	TAILQ_INIT(&dead);
	vm_map_lock(smap);
	uvm_unmap_remove(smap, saddr, saddr + len, &dead, FALSE, TRUE, FALSE);
	vm_map_unlock(smap);
	uvm_unmap_detach(&dead, 0);

	sendnum_daddr = daddr;
	sendnum_flags |= TRANSFER_DONE;
	wakeup(&sendnum_flags);

	return (0);
}

int
sys_sendnum(struct proc *p, void *v, register_t *retval)
{
	struct sys_sendnum_args *uap = v;
	int eno;

	mtx_enter(&sendnum_mtx);
	if (sendnum_flags & (SEND_WAITING | TRANSFER_DONE)) {
		eno = EBUSY;
		goto out;
	}

	sendnum_flags |= SEND_WAITING;
	sendnum_sender = p;
	sendnum_saddr = (vaddr_t)SCARG(uap, addr);
	sendnum_len = SCARG(uap, len);

	eno = sendnum_finish();
	if (eno != 0 && eno != EAGAIN) {
		sendnum_flags &= ~SEND_WAITING;
		sendnum_sender = NULL;
		goto out;
	}

	while (!(sendnum_flags & TRANSFER_DONE)) {
		eno = msleep(&sendnum_flags, &sendnum_mtx, PCATCH,
		    "sendnum", 0);
		if (eno != 0) {
			sendnum_flags &= ~SEND_WAITING;
			sendnum_sender = NULL;
			goto out;
		}
	}

	sendnum_flags &= ~SEND_WAITING;
	if (!(sendnum_flags & RECV_WAITING))
		sendnum_flags &= ~TRANSFER_DONE;

	eno = 0;

out:
	mtx_leave(&sendnum_mtx);
	return (eno);
}

int
sys_recvnum(struct proc *p, void *v, register_t *retval)
{
	struct sys_recvnum_args *uap = v;
	int eno;

	mtx_enter(&sendnum_mtx);

	if (sendnum_flags & (RECV_WAITING | TRANSFER_DONE)) {
		eno = EBUSY;
		goto out;
	}

	sendnum_flags |= RECV_WAITING;
	sendnum_receiver = p;

	eno = sendnum_finish();
	if (eno != 0 && eno != EAGAIN) {
		sendnum_flags &= ~RECV_WAITING;
		sendnum_receiver = NULL;
		goto out;
	}

	while (!(sendnum_flags & TRANSFER_DONE)) {
		eno = msleep(&sendnum_flags, &sendnum_mtx, PCATCH,
		    "recvnum", 0);
		if (eno != 0) {
			sendnum_flags &= ~RECV_WAITING;
			sendnum_receiver = NULL;
			goto out;
		}
	}

	sendnum_flags &= ~RECV_WAITING;
	if (!(sendnum_flags & SEND_WAITING))
		sendnum_flags &= ~TRANSFER_DONE;

	eno = copyout(&sendnum_daddr, SCARG(uap, addr), sizeof(void *));
	if (eno)
		goto out;
	eno = copyout(&sendnum_len, SCARG(uap, len), sizeof(size_t));
	if (eno)
		goto out;

	eno = 0;

out:
	mtx_leave(&sendnum_mtx);
	return (eno);
}