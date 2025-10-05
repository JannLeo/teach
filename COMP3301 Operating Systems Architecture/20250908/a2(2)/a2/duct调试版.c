#include <sys/param.h>
#include <sys/systm.h>
#include <sys/errno.h>
#include <sys/ioctl.h>
#include <sys/fcntl.h>
#include <sys/device.h>
#include <sys/vnode.h>
#include <sys/atomic.h>
#include <sys/event.h>
#include <sys/mutex.h>
#include <sys/select.h>
#include <sys/selinfo.h>
#include <sys/signalvar.h>
#include <sys/uio.h>
#include <sys/proc.h>
#include <sys/systm.h>

#include <machine/bus.h>
#include <machine/intrdefs.h>
#include <machine/endian.h>

#include <dev/pci/pcireg.h>
#include <dev/pci/pcivar.h>
#include <dev/pci/pcidevs.h>


#include <dev/ductvar.h>

/* ======================== Device registers ======================== */
#define A2_REG_VMAJ       0x00    /* major version register (RO) */
#define A2_REG_VMIN       0x04    /* minor version register (RO) */
#define A2_REG_FLAGS      0x08    /* FLAGS register: error + reset */
#define A2_REG_HWADDR     0x0C    /* hardware address */
#define A2_REG_CMDBASE    0x10    /* command ring base address */
#define A2_REG_CMDSHIFT   0x18    /* command ring size shift */
#define A2_REG_TXBASE     0x20    /* transmit ring base address */
#define A2_REG_TXSHIFT    0x28    /* transmit ring size shift */
#define A2_REG_RXBASE     0x30    /* receive ring base address */
#define A2_REG_RXSHIFT    0x38    /* receive ring size shift */
#define A2_REG_EVFLAGS    0x40    /* event flags register (read-to-clear) */
#define A2_REG_DBELL      0x50    /* doorbell register */

/* ======================== Device error flags ========================= */
/*
 * FLAGS register (A2_REG_FLAGS) bits. Fatal errors cause the device to stop
 * and require reset. When any of these bits are set, the driver must enter
 * DUCT_S_ERROR and all user operations should fail with EIO.
 */
#define A2_FLAGS_FLTB    (1U << 0)   /* fault in BAR-provided pointer */
#define A2_FLAGS_FLTR    (1U << 1)   /* fault in descriptor ring pointer */
#define A2_FLAGS_SEQ     (1U << 2)   /* out-of-sequence operation */
#define A2_FLAGS_HWERR   (1U << 16)  /* miscellaneous hardware error */
#define A2_FLAGS_RST     (1U << 31)  /* reset bit (write 1 to reset) */

/* ======================== Command descriptor errors ================== */
/*
 * a2cd_err field (in struct a2_cmd_desc).
 * These codes indicate per-command failures. Unlike FLAGS errors, the device
 * remains operational; ioctl(2) calls should translate these into errno.
 */
#define A2_ERR_OK        0x00   /* success */
#define A2_ERR_INVAL     0x01   /* invalid argument (not multicast) */
#define A2_ERR_NOSPC     0x02   /* no space for new filter */
#define A2_ERR_NOENT     0x03   /* no matching filter */
#define A2_ERR_HWERR     0xFF   /* generic hardware error */

/* Mapping from A2_ERR_* to user-visible errno: 
 *   A2_ERR_INVAL to EINVAL
 *   A2_ERR_NOSPC to ENOSPC
 *   A2_ERR_NOENT to ENOENT
 *   A2_ERR_HWERR to EIO
 */

/* Event flags (EVFLAGS register, section 6.5 Handling events) */
#define A2_EV_TXCOMP      (1U << 0)  /* TX completion event */
#define A2_EV_RXCOMP      (1U << 1)  /* RX completion event */
#define A2_EV_CMDCOMP     (1U << 2)  /* command completion event */
#define A2_EV_RXDROP      (1U << 3)  /* RX drop event */
#define A2_EV_RXJUMBO     (1U << 4)  /* RX jumbo event */

/* ================= Descriptor ownership / status ================== */
/* Spec section 6.4 says OWNER is one byte: 0x55 = DEVICE, 0xAA = HOST */
#define A2_OWNER_DEVICE   0x55  /* owned by device */
#define A2_OWNER_HOST     0xAA  /* owned by host */

/* ======================== Command types =========================== */
#define A2_CMD_START      0x00000001U  /* start normal packet operation */
#define A2_CMD_STOP       0x00000002U  /* stop normal operation */
#define A2_CMD_ADDFILT    0x00000003U  /* add an address filter */
#define A2_CMD_RMFILT     0x00000004U  /* remove an address filter */
#define A2_CMD_FLUSHFILT  0x00000005U  /* remove all filters */

/* Command descriptor structure (32 bytes) - spec section 6.4 */
/* Command descriptor (32 bytes, section 6.4) */
struct a2_cmd_desc {
	uint8_t     a2cd_owner;   /* OWNER: 0x55=DEV, 0xAA=HOST */
	uint8_t     a2cd_type; 
	uint8_t     a2cd_err;     /* error code (if any) */
	uint8_t     a2cd_reserved0[5];    /* reserved */
	uint32_t    a2cd_filtmask;    /* filter mask */
	uint32_t    a2cd_filtaddr;    /* filter address */
	uint64_t    a2cd_reserved1[2]; /* reserved (16 bytes) */
}__packed;
CTASSERT(sizeof(struct a2_cmd_desc) == 32);

/* RX descriptor (64 bytes, section 6.6) */
struct a2_rx_desc {
	uint8_t     a2rd_owner;   /* OWNER: 0x55=DEV, 0xAA=HOST */
	uint8_t     a2rd_reserved0[3];    /* reserved */
	uint32_t    a2rd_pktlen;  /* packet total length */
	uint32_t    a2rd_length[4]; /* scatter lengths */
	uint32_t    a2rd_dst;     /* destination address */
	uint32_t    a2rd_src;     /* source address */
	uint64_t    a2rd_ptr[4];  /* buffer physical addresses */
}__packed;
CTASSERT(sizeof(struct a2_rx_desc) == 64);


/* TX descriptor (64 bytes, section 6.7) */
struct a2_tx_desc {
	uint8_t     a2td_owner;   /* OWNER: 0x55=DEV, 0xAA=HOST */
	uint8_t     a2td_reserved0[3];    /* reserved */
	uint32_t    a2td_pktlen;  /* total packet length */
	uint32_t    a2td_length[4]; /* scatter lengths */
	uint32_t    a2td_dst;     /* destination address */
	uint32_t    a2td_src;     /* not used for TX */
	uint64_t    a2td_ptr[4];  /* buffer physical addresses */
}__packed;
CTASSERT(sizeof(struct a2_tx_desc) == 64);

/* Device states */
#define DUCT_S_STOPPED    0  /* device stopped */
#define DUCT_S_STARTING   1  /* device starting */
#define DUCT_S_RUNNING    2  /* device running */
#define DUCT_S_STOPPING   3  /* device stopping */
#define DUCT_S_ERROR      4  /* device error */

struct duct_softc {
	struct device		 sc_dev;   /* OpenBSD device header */
	
	/* PCI / bus space */
	pci_chipset_tag_t	 sc_pc;    /* PCI chipset handle */
	pcitag_t		     sc_tag;   /* PCI device tag */
	bus_space_tag_t		 sc_iot;   /* MMIO tag */
	bus_space_handle_t	 sc_ioh;   /* MMIO handle */
	bus_size_t		     sc_iosize;/* BAR0 mapping size */
	bus_dma_tag_t		 sc_dmat;  /* DMA tag */
	
	/* cached read-only information */
	uint32_t		 sc_vmaj, sc_vmin; /* version numbers */
	uint32_t		 sc_hwaddr;       /* hardware address */
	
	/* MSI-X interrupt handles */
	pci_intr_handle_t	 sc_ih_ev;   /* event interrupt handle */
	pci_intr_handle_t	 sc_ih_err;  /* error interrupt handle */
	void			*sc_ihc_ev;  /* event interrupt context */
	void			*sc_ihc_err; /* error interrupt context */
	
	/* command ring */
	bus_dmamap_t		 sc_cmd_map; /* command ring DMA map */
	bus_dma_segment_t	 sc_cmd_seg; /* command ring DMA segment */
	void			    *sc_cmd_kva; /* command ring kernel virtual address */
	paddr_t		 sc_cmd_pa;   /* command ring physical address */
	u_int		 sc_cmd_prod; /* producer index */
	u_int		 sc_cmd_cons; /* consumer index */
	u_int		 sc_cmd_size; /* command ring size */
	u_int		 sc_cmd_pending; /* pending command count */
	int          sc_cmd_errno;   /* errno for last completed command */
	
	/* RX ring */
	bus_dmamap_t		 sc_rx_map;  /* RX ring DMA map */
	bus_dma_segment_t	 sc_rx_seg;  /* RX ring DMA segment */
	void			    *sc_rx_kva;  /* RX ring kernel virtual address */
	paddr_t		 sc_rx_pa;    /* RX ring physical address */
	u_int		 sc_rx_prod;  /* producer index */
	u_int		 sc_rx_cons;  /* consumer index */
	u_int		 sc_rx_size;  /* RX ring size */
	
	/* RX buffers */
	bus_dmamap_t		*sc_rx_buf_maps; /* RX buffer DMA maps */
	void			   **sc_rx_buf_kva;  /* RX buffer KVAs */
	paddr_t			    *sc_rx_buf_pa;    /* RX buffer PAs */
	bus_dma_segment_t	*sc_rx_buf_segs; /* RX buffer DMA segments */
	u_int			     sc_rx_buf_size;   /* buffer size */
	
	/* TX ring */
	bus_dmamap_t		sc_tx_map;  /* TX ring DMA map */
	bus_dma_segment_t	sc_tx_seg;  /* TX ring DMA segment */
	void			*sc_tx_kva;  /* TX ring kernel virtual address */
	paddr_t			sc_tx_pa;    /* TX ring physical address */
	u_int			sc_tx_prod;  /* producer index */
	u_int			sc_tx_cons;  /* consumer index */
	u_int			sc_tx_size;  /* TX ring size */
	
	/* TX buffers */
	bus_dmamap_t		*sc_tx_buf_maps; /* TX buffer DMA maps */
	void			   **sc_tx_buf_kva;  /* TX buffer KVAs */
	paddr_t			    *sc_tx_buf_pa;    /* TX buffer PAs */
	bus_dma_segment_t	*sc_tx_buf_segs; /* TX buffer DMA segments */
	u_int			     sc_tx_buf_size;   /* buffer size */
	
	/* character device related */
	struct klist		 sc_klist;   /* kqueue listener list */
	struct selinfo		 sc_selinfo; /* select/poll support */
	struct mutex		 sc_mtx;     /* mutex protection */
	int			         sc_open;    /* number of active opens (reference count) */
	
	/* wait queues */
	void			    *sc_tx_queue; /* TX completion wait queue */
	unsigned int		 sc_state;   /* device state */
	
	/* RX packet queue */
	struct duct_packet_hdr	*sc_rx_queue;  /* RX packet queue */
	void		   **sc_rx_payload; /* RX payload queue */
	u_int			*sc_rx_payload_len; /* RX payload lengths */
	u_int			 sc_rx_qhead;   /* queue head */
	u_int			 sc_rx_qtail;   /* queue tail */
	u_int			 sc_rx_qsize;   /* queue size */
};

/* Forward declarations */
int	duct_match(struct device *, void *, void *);
void	duct_attach(struct device *, struct device *, void *);
int	duct_detach(struct device *, int);

/* Character device functions */
int	ductopen(dev_t, int, int, struct proc *);
int	ductclose(dev_t, int, int, struct proc *);
int	ductread(dev_t, struct uio *, int);
int	ductwrite(dev_t, struct uio *, int);
int	ductioctl(dev_t, u_long, caddr_t, int, struct proc *);
int	ductkqfilter(dev_t, struct knote *);

/* Device lookup */
static struct duct_softc *duct_lookup(dev_t);

/* Kqueue support */
int	duct_read_event(struct knote *, long);
int	duct_write_event(struct knote *, long);
void	duct_kqdetach(struct knote *);
int	duct_filt_process(struct knote *, struct kevent *);

/* Interrupt handlers */
int	duct_intr_event(void *);
int	duct_intr_error(void *);

/* Command ring functions */
int	duct_cmd_alloc(struct duct_softc *);
void	duct_cmd_free(struct duct_softc *);
int	duct_cmd_submit(struct duct_softc *, uint32_t, uint32_t, uint32_t);
void	duct_cmd_process(struct duct_softc *);

/* RX ring functions */
int	duct_rx_alloc(struct duct_softc *);
void	duct_rx_free(struct duct_softc *);
void	duct_rx_process(struct duct_softc *);

/* TX ring functions */
int	duct_tx_alloc(struct duct_softc *);
void	duct_tx_free(struct duct_softc *);
void	duct_tx_process(struct duct_softc *);
int	duct_tx_submit(struct duct_softc *, const void *, size_t);

/* Utility functions */
static void ring_reinit_rx(struct duct_softc *);
static void ring_reinit_tx(struct duct_softc *);

/* ========================= CFATTACH =================================== */
const struct cfattach duct_ca = {
	sizeof(struct duct_softc), duct_match, duct_attach, duct_detach
};

struct cfdriver duct_cd = {
	NULL, "duct", DV_DULL
};

const struct pci_matchid duct_devices[] = {
	{ 0x3301, 0x2000 }  /* COMP3301 duct device */
};

/* Kqueue filter operations */
const struct filterops duct_read_filtops = {
	.f_flags  = FILTEROP_ISFD,
	.f_attach = NULL,               
	.f_detach = duct_kqdetach,
	.f_event  = duct_read_event,
	.f_modify = NULL,
	.f_process= duct_filt_process,
};

const struct filterops duct_write_filtops = {
	.f_flags  = FILTEROP_ISFD,
	.f_attach = NULL,
	.f_detach = duct_kqdetach,
	.f_event  = duct_write_event,
	.f_modify = NULL,
	.f_process = duct_filt_process,
};

/* ========================= MATCH/ATTACH ============================== */
int
duct_match(struct device *parent, void *match, void *aux)
{
	struct pci_attach_args *pa = aux;
	return (pci_matchbyid(pa, duct_devices, nitems(duct_devices)));
}

void
duct_attach(struct device *parent, struct device *self, void *aux)
{
	struct duct_softc *sc = (struct duct_softc *)self;
	struct pci_attach_args *pa = aux;

	printf(": duct driver starting initialization\n");

	sc->sc_pc = pa->pa_pc;
	sc->sc_tag = pa->pa_tag;
	sc->sc_dmat = pa->pa_dmat;

	/* Initializing state and locks */
	sc->sc_state = DUCT_S_STOPPED;
	mtx_init(&sc->sc_mtx, IPL_BIO);

	/* Mapping BAR0 (MEM32) */
	if (pci_mapreg_map(pa, PCI_MAPREG_START,
	    PCI_MAPREG_TYPE_MEM | PCI_MAPREG_MEM_TYPE_32BIT, 0,
	    &sc->sc_iot, &sc->sc_ioh, NULL, &sc->sc_iosize, 0)) {
		printf(": can't map BAR0\n");
		goto unmap;
	}
	printf(": BAR0 mapped successfully, size=%zu\n", sc->sc_iosize);

	/* Enable bus mastering and allow DMA */
	pcireg_t csr = pci_conf_read(sc->sc_pc, sc->sc_tag,
	                             PCI_COMMAND_STATUS_REG);
	csr |= PCI_COMMAND_MASTER_ENABLE | PCI_COMMAND_MEM_ENABLE;
	pci_conf_write(sc->sc_pc, sc->sc_tag,
	               PCI_COMMAND_STATUS_REG, csr);
	csr = pci_conf_read(sc->sc_pc, sc->sc_tag, PCI_COMMAND_STATUS_REG);
	printf(": PCI CMD=0x%08x (bus mastering %s)\n",
	    csr, (csr & PCI_COMMAND_MASTER_ENABLE) ? "on" : "OFF");

	/* Read version number and hardware address */
	sc->sc_vmaj = bus_space_read_4(sc->sc_iot, sc->sc_ioh, A2_REG_VMAJ);
	sc->sc_vmin = bus_space_read_4(sc->sc_iot, sc->sc_ioh, A2_REG_VMIN);
	sc->sc_hwaddr = bus_space_read_4(sc->sc_iot, sc->sc_ioh, A2_REG_HWADDR);
	printf(": A2 v%u.%u hwaddr=0x%08x\n",
	    sc->sc_vmaj, sc->sc_vmin, sc->sc_hwaddr);

	if (sc->sc_vmaj == 0 && sc->sc_vmin == 0) {
		printf(": invalid version numbers\n");
		goto unmap;
	}

	/* Configuring MSI-X interrupts */
	if (pci_intr_map_msix(pa, 0, &sc->sc_ih_ev) != 0) {
		printf(": unable to map MSI-X event interrupt\n");
		goto unmap;
	}
	if (pci_intr_map_msix(pa, 1, &sc->sc_ih_err) != 0) {
		printf(": unable to map MSI-X error interrupt\n");
		goto unmap;
	}

	sc->sc_ihc_ev = pci_intr_establish(sc->sc_pc, sc->sc_ih_ev,
	    IPL_BIO, duct_intr_event, sc, sc->sc_dev.dv_xname);
	if (sc->sc_ihc_ev == NULL) {
		printf(": unable to establish event interrupt\n");
		goto unmap;
	}
	sc->sc_ihc_err = pci_intr_establish(sc->sc_pc, sc->sc_ih_err,
	    IPL_BIO, duct_intr_error, sc, sc->sc_dev.dv_xname);
	if (sc->sc_ihc_err == NULL) {
		printf(": unable to establish error interrupt\n");
		pci_intr_disestablish(sc->sc_pc, sc->sc_ihc_ev);
		goto unmap;
	}
	
	(void)bus_space_read_4(sc->sc_iot, sc->sc_ioh, A2_REG_EVFLAGS);
	printf(": configured device to use MSI-X vector 0 for events\n");
	
	/* Check FLAGS register and reset if necessary */
	uint32_t flags = bus_space_read_4(sc->sc_iot, sc->sc_ioh, A2_REG_FLAGS);
	printf(": current FLAGS=0x%08x\n", flags);
	
	/* If FLAGS non-zero, reset per specification */
	if (flags != 0) {
		printf(": FLAGS non-zero, resetting device\n");
		/* Write RST bit to FLAGS register */
		bus_space_write_4(sc->sc_iot, sc->sc_ioh, A2_REG_FLAGS, 0x80000000);
		bus_space_barrier(sc->sc_iot, sc->sc_ioh, A2_REG_FLAGS, 4, BUS_SPACE_BARRIER_WRITE);
		
		/* Poll until FLAGS becomes 0 (reset complete) */
		for (int t = 0; t < 1000000; t++) {
			flags = bus_space_read_4(sc->sc_iot, sc->sc_ioh, A2_REG_FLAGS);
			if (flags == 0) {
				printf(": device reset completed successfully\n");
				break;
			}
			delay(1);
		}
		if (flags != 0) {
			printf(": device reset timeout, FLAGS=0x%08x\n", flags);
			goto unmap;
		}
	}

	/* Allocate rings */
    if (duct_cmd_alloc(sc) != 0 ||
        duct_rx_alloc(sc) != 0 ||
        duct_tx_alloc(sc) != 0) {
        printf(": failed to allocate rings\n");
        goto unmap;
    }

    /* Set ring base/shift */
    bus_space_write_8(sc->sc_iot, sc->sc_ioh, A2_REG_CMDBASE, sc->sc_cmd_pa);
    bus_space_write_4(sc->sc_iot, sc->sc_ioh, A2_REG_CMDSHIFT,
        flsl(sc->sc_cmd_size) - 1);

    bus_space_write_8(sc->sc_iot, sc->sc_ioh, A2_REG_RXBASE, sc->sc_rx_pa);
    bus_space_write_4(sc->sc_iot, sc->sc_ioh, A2_REG_RXSHIFT,
        flsl(sc->sc_rx_size) - 1);

    bus_space_write_8(sc->sc_iot, sc->sc_ioh, A2_REG_TXBASE, sc->sc_tx_pa);
    bus_space_write_4(sc->sc_iot, sc->sc_ioh, A2_REG_TXSHIFT,
        flsl(sc->sc_tx_size) - 1);

    /* ---------------- character device initialization ---------------- */
    klist_init(&sc->sc_klist, NULL, NULL);
    sc->sc_open = 0;            /* refcount, not boolean */
    sc->sc_state = DUCT_S_STOPPED;
    sc->sc_cmd_errno = 0;       /* last command errno */

    /* Initialize the RX queue */
    sc->sc_rx_qsize = 64;
    sc->sc_rx_queue = mallocarray(sc->sc_rx_qsize,
        sizeof(struct duct_packet_hdr), M_DEVBUF, M_WAITOK | M_ZERO);
    sc->sc_rx_payload = mallocarray(sc->sc_rx_qsize,
        sizeof(void *), M_DEVBUF, M_WAITOK | M_ZERO);
    sc->sc_rx_payload_len = mallocarray(sc->sc_rx_qsize,
        sizeof(u_int), M_DEVBUF, M_WAITOK | M_ZERO);
    sc->sc_rx_qhead = sc->sc_rx_qtail = 0;

    printf(": duct driver initialized successfully\n");
    return;

unmap:
	if (sc->sc_iosize)
		bus_space_unmap(sc->sc_iot, sc->sc_ioh, sc->sc_iosize);
	sc->sc_iosize = 0;
}

int
duct_detach(struct device *self, int flags)
{
	struct duct_softc *sc = (struct duct_softc *)self;
	
	if (sc->sc_open != 0)
        printf("%s: detaching while still %d opens active\n",
            sc->sc_dev.dv_xname, sc->sc_open);

	printf(": duct driver detaching\n");
	
	/* Disestablish interrupts */
	if (sc->sc_ihc_ev)
		pci_intr_disestablish(sc->sc_pc, sc->sc_ihc_ev);
	if (sc->sc_ihc_err)
		pci_intr_disestablish(sc->sc_pc, sc->sc_ihc_err);
	
	/* Free RX queue */
	if (sc->sc_rx_queue) {
		free(sc->sc_rx_queue, M_DEVBUF, sc->sc_rx_qsize * sizeof(struct duct_packet_hdr));
		sc->sc_rx_queue = NULL;
	}
	if (sc->sc_rx_payload) {
		/* Free any remaining payload buffers */
		for (int i = 0; i < sc->sc_rx_qsize; i++) {
			if (sc->sc_rx_payload[i]) {
				free(sc->sc_rx_payload[i], M_DEVBUF, sc->sc_rx_payload_len[i]);
			}
		}
		free(sc->sc_rx_payload, M_DEVBUF, sc->sc_rx_qsize * sizeof(void *));
		sc->sc_rx_payload = NULL;
	}
	if (sc->sc_rx_payload_len) {
		free(sc->sc_rx_payload_len, M_DEVBUF, sc->sc_rx_qsize * sizeof(u_int));
		sc->sc_rx_payload_len = NULL;
	}
	
	/* Free TX ring */
	duct_tx_free(sc);
	
	/* Free RX ring */
	duct_rx_free(sc);
	
	/* Free command ring */
	duct_cmd_free(sc);
	
	/* Cleanup character device resources */
	/* selinfo cleanup handled automatically by system */
	/* mutex cleanup handled automatically */
	
	if (sc->sc_iosize)
		bus_space_unmap(sc->sc_iot, sc->sc_ioh, sc->sc_iosize);
	sc->sc_iosize = 0;
	
	return 0;
}

/* ========================= CHARACTER DEVICE ========================== */
static struct duct_softc *
duct_lookup(dev_t dev)
{
	/* the device minor is 1:1 with the driver unit number */
	dev_t unit = minor(dev);
	struct duct_softc *sc;
	
	if (unit >= duct_cd.cd_ndevs)
		return (NULL);
	
	/* this will be NULL if there's no device */
	sc = duct_cd.cd_devs[unit];
	
	return (sc);
}

int
ductopen(dev_t dev, int mode, int flags, struct proc *p)
{
    struct duct_softc *sc = duct_lookup(dev);
    int error = 0;

    if (sc == NULL)
        return (ENXIO);

    mtx_enter(&sc->sc_mtx);

    if (sc->sc_state == DUCT_S_ERROR) {
        mtx_leave(&sc->sc_mtx);
        printf("%s: device is in error state\n", sc->sc_dev.dv_xname);
        return (ENXIO);   /* only ENXIO/ENOMEM allowed here */
    }

    sc->sc_open++;
    /* If it is not the first open, return directly */
    if (sc->sc_open > 1) {
        mtx_leave(&sc->sc_mtx);
        return (0);
    }
    mtx_leave(&sc->sc_mtx);

    /* First open: Start the device */
    printf("%s: sending START command\n", sc->sc_dev.dv_xname);
    error = duct_cmd_submit(sc, A2_CMD_START, 0, 0);
    if (error != 0) {
        printf("%s: START submit failed (%d)\n", sc->sc_dev.dv_xname, error);
        return (ENOMEM); 
    }

    /* Ring the doorbell */
    uint32_t idx = (sc->sc_cmd_prod - 1) & (sc->sc_cmd_size - 1);
    bus_space_write_4(sc->sc_iot, sc->sc_ioh, A2_REG_DBELL, idx);

    /* Adding a unicast filter */
    printf("%s: adding unicast filter\n", sc->sc_dev.dv_xname);
    error = duct_cmd_submit(sc, A2_CMD_ADDFILT, 0xFFFFFFFFU, sc->sc_hwaddr);
    if (error != 0) {
        printf("%s: ADDFILT submit failed (%d)\n", sc->sc_dev.dv_xname, error);
        return (ENOMEM);
    }
    idx = (sc->sc_cmd_prod - 1) & (sc->sc_cmd_size - 1);
    bus_space_write_4(sc->sc_iot, sc->sc_ioh, A2_REG_DBELL, idx);

    /* Waiting for device RUNNING*/
    mtx_enter(&sc->sc_mtx);
    while (sc->sc_state != DUCT_S_RUNNING) {
        mtx_leave(&sc->sc_mtx);
        error = tsleep(&sc->sc_state, PZERO | PCATCH, "ductopen", 0);
        if (error != 0)
            return (error);
        mtx_enter(&sc->sc_mtx);
    }
    mtx_leave(&sc->sc_mtx);

    printf("%s: device running, open complete\n", sc->sc_dev.dv_xname);
    return (0);
}

int
ductclose(dev_t dev, int flags, int mode, struct proc *p)
{
    struct duct_softc *sc = duct_lookup(dev);
    int error;

    if (sc == NULL)
        return (ENXIO);

    mtx_enter(&sc->sc_mtx);
    sc->sc_open--;
    if (sc->sc_open > 0) {
        mtx_leave(&sc->sc_mtx);
        return (0); /* There are other fds open, do not do STOP */
    }
    mtx_leave(&sc->sc_mtx);

    /* Clear multicast filters when the last fd is closed */
    printf("%s: flushing multicast filters\n", sc->sc_dev.dv_xname);
    error = duct_cmd_submit(sc, A2_CMD_FLUSHFILT, 0, 0);
    if (error == 0) {
        uint32_t idx = (sc->sc_cmd_prod - 1) & (sc->sc_cmd_size - 1);
        bus_space_write_4(sc->sc_iot, sc->sc_ioh, A2_REG_DBELL, idx);
    } else {
        printf("%s: failed to flush filters (%d)\n", sc->sc_dev.dv_xname, error);
    }

    /* STOP device */
    printf("%s: sending STOP command\n", sc->sc_dev.dv_xname);
    error = duct_cmd_submit(sc, A2_CMD_STOP, 0, 0);
    if (error == 0) {
        uint32_t idx = (sc->sc_cmd_prod - 1) & (sc->sc_cmd_size - 1);
        bus_space_write_4(sc->sc_iot, sc->sc_ioh, A2_REG_DBELL, idx);

        mtx_enter(&sc->sc_mtx);
        while (sc->sc_state != DUCT_S_STOPPED) {
            mtx_leave(&sc->sc_mtx);
            (void)tsleep(&sc->sc_state, PZERO, "ductstop", 0);
            mtx_enter(&sc->sc_mtx);
        }
        mtx_leave(&sc->sc_mtx);

        ring_reinit_rx(sc);
        ring_reinit_tx(sc);
    } else {
        printf("%s: STOP submit failed (%d)\n", sc->sc_dev.dv_xname, error);
    }

    printf("%s: close complete\n", sc->sc_dev.dv_xname);
    return (0); 
}

int
ductread(dev_t dev, struct uio *uio, int ioflag)
{
    struct duct_softc *sc = duct_lookup(dev);
    struct duct_packet_hdr *pkt_hdr;
    void *payload;
    u_int payload_len;
    int error = 0;

    if (sc == NULL)
        return (ENXIO);

    /* Hardware error checking */
    if (sc->sc_state == DUCT_S_ERROR)
        return (EIO);

    mtx_enter(&sc->sc_mtx);

    if (ioflag & O_NONBLOCK) {
        if (sc->sc_rx_qhead == sc->sc_rx_qtail) {
            mtx_leave(&sc->sc_mtx);
            return (EAGAIN);
        }
    } else {
        while (sc->sc_rx_qhead == sc->sc_rx_qtail) {
            mtx_leave(&sc->sc_mtx);
            error = tsleep(&sc->sc_rx_queue, PZERO | PCATCH, "ductread", 0);
            if (error != 0)
                return (error);
            mtx_enter(&sc->sc_mtx);
        }
    }

    pkt_hdr = &sc->sc_rx_queue[sc->sc_rx_qhead];
    payload = sc->sc_rx_payload[sc->sc_rx_qhead];
    payload_len = sc->sc_rx_payload_len[sc->sc_rx_qhead];
    sc->sc_rx_qhead = (sc->sc_rx_qhead + 1) & (sc->sc_rx_qsize - 1);

    mtx_leave(&sc->sc_mtx);

    /* Copy the header first */
    error = uiomove(pkt_hdr, sizeof(*pkt_hdr), uio);
    if (error != 0) {
        if (payload) free(payload, M_DEVBUF, payload_len);
        return (error);
    }

    /* Copy the payload again*/
    if (payload && payload_len > 0) {
        size_t to_copy = MIN(payload_len, uio->uio_resid);
        if (to_copy > 0) {
            error = uiomove(payload, to_copy, uio);
        }
        /* If the buffer is insufficient, the remaining data is discarded. */
        if (to_copy < payload_len) {
            printf("%s: read buffer too small, dropped %zu bytes\n",
                sc->sc_dev.dv_xname, (size_t)payload_len - to_copy);
        }
        free(payload, M_DEVBUF, payload_len);
        if (error != 0) return (error);
    }

    return (0);
}


int
ductwrite(dev_t dev, struct uio *uio, int ioflag)
{
    struct duct_softc *sc = duct_lookup(dev);
    struct duct_packet_hdr hdr;
    char *kbuf = NULL;
    size_t total_len;
    int error = 0;

    if (sc == NULL)
        return (ENXIO);

    /* Hardware Error Checking */
    if (sc->sc_state == DUCT_S_ERROR)
        return (EIO);

    /* Must have at least header */
    if (uio->uio_resid < sizeof(hdr))
        return (EINVAL);

    /* Read the header first */
    error = uiomove(&hdr, sizeof(hdr), uio);
    if (error != 0)
        return (error);

    /* Verify payload length */
    if (hdr.dpkt_length > (sc->sc_tx_buf_size - sizeof(hdr)))
        return (EINVAL);

    total_len = sizeof(hdr) + hdr.dpkt_length;
    if (total_len > 16384)
        return (EINVAL);

    /* Allocating kernel buffers*/
    kbuf = malloc(total_len, M_DEVBUF, M_WAITOK);
    KASSERT(kbuf != NULL);

    /* Copy header */
    memcpy(kbuf, &hdr, sizeof(hdr));

    /* Copy payload from user mode */
    if (hdr.dpkt_length > 0) {
        size_t before = uio->uio_resid;
        error = uiomove(kbuf + sizeof(hdr), hdr.dpkt_length, uio);
        size_t after = uio->uio_resid;
        size_t copied = before - after;

        if (error != 0 || copied != hdr.dpkt_length) {
            free(kbuf, M_DEVBUF, total_len);
            return (EINVAL);   /* Length does not match header */
        }
    }

    /* Check TX ring space */
    mtx_enter(&sc->sc_mtx);
    u_int next_prod = (sc->sc_tx_prod + 1) % sc->sc_tx_size;
    while (next_prod == sc->sc_tx_cons) {
        /* TX ring full */
        if (ioflag & O_NONBLOCK) {
            mtx_leave(&sc->sc_mtx);
            free(kbuf, M_DEVBUF, total_len);
            return (EAGAIN);
        }
        /* Blocking wait, can be interrupted by signal */
        error = tsleep(&sc->sc_tx_queue, PZERO | PCATCH, "ductwrite", 0);
        if (error != 0) {
            mtx_leave(&sc->sc_mtx);
            free(kbuf, M_DEVBUF, total_len);
            return (error);  /* EINTR */
        }
        next_prod = (sc->sc_tx_prod + 1) % sc->sc_tx_size;
    }
    mtx_leave(&sc->sc_mtx);

    /* Submit to TX Ring */
    error = duct_tx_submit(sc, kbuf, total_len);
    free(kbuf, M_DEVBUF, total_len);
    if (error != 0)
        return (error);

    return (0);
}


int
ductioctl(dev_t dev, u_long cmd, caddr_t data, int flag, struct proc *p)
{
    struct duct_softc *sc = duct_lookup(dev);
    int error = 0;

    if (sc == NULL)
        return (ENXIO);

    /* Fatal device error: all ops fail with EIO. */
    if (sc->sc_state == DUCT_S_ERROR)
        return (EIO);

    switch (cmd) {
    case DUCTIOC_GET_INFO: {
        struct duct_info_arg *info = (struct duct_info_arg *)data;
        info->duct_major  = sc->sc_vmaj;
        info->duct_minor  = sc->sc_vmin;
        info->duct_hwaddr = sc->sc_hwaddr;
        return 0;
    }

    case DUCTIOC_ADD_MCAST: {
        struct duct_mcast_arg *mcast = (struct duct_mcast_arg *)data;

        /* Multicast address check: highest bit must be 1. */
        if ((mcast->duct_addr & 0x80000000U) == 0)
            return (EINVAL);

        /* Submit command; treat submission failure as hw error. */
        error = duct_cmd_submit(sc, A2_CMD_ADDFILT,
            mcast->duct_mask, mcast->duct_addr);
        if (error != 0)
            return (EIO);

        /* Ring doorbell for CMD (no high bit for CMD). */
        uint32_t idx = (sc->sc_cmd_prod - 1) & (sc->sc_cmd_size - 1);
        bus_space_write_4(sc->sc_iot, sc->sc_ioh, A2_REG_DBELL, idx);

        /* Wait for completion (interruptible). */
        mtx_enter(&sc->sc_mtx);
        while (sc->sc_cmd_pending > 0) {
            mtx_leave(&sc->sc_mtx);
            error = tsleep(&sc->sc_cmd_cons, PZERO | PCATCH, "addmcast", 0);
            if (error != 0)
                return (error); /* EINTR allowed */
            mtx_enter(&sc->sc_mtx);
        }
        mtx_leave(&sc->sc_mtx);

        if (sc->sc_state == DUCT_S_ERROR)
            return (EIO);
        return sc->sc_cmd_errno; /* 0 / EINVAL / ENOSPC / EIO */
    }

    case DUCTIOC_RM_MCAST: {
        struct duct_mcast_arg *mcast = (struct duct_mcast_arg *)data;

        if ((mcast->duct_addr & 0x80000000U) == 0)
            return (EINVAL);

        error = duct_cmd_submit(sc, A2_CMD_RMFILT,
            mcast->duct_mask, mcast->duct_addr);
        if (error != 0)
            return (EIO);

        uint32_t idx = (sc->sc_cmd_prod - 1) & (sc->sc_cmd_size - 1);
        bus_space_write_4(sc->sc_iot, sc->sc_ioh, A2_REG_DBELL, idx);

        mtx_enter(&sc->sc_mtx);
        while (sc->sc_cmd_pending > 0) {
            mtx_leave(&sc->sc_mtx);
            error = tsleep(&sc->sc_cmd_cons, PZERO | PCATCH, "rmmcast", 0);
            if (error != 0)
                return (error);
            mtx_enter(&sc->sc_mtx);
        }
        mtx_leave(&sc->sc_mtx);

        if (sc->sc_state == DUCT_S_ERROR)
            return (EIO);
        return sc->sc_cmd_errno; /* 0 / EINVAL / ENOENT / EIO */
    }

    default:
        return (ENOTTY);
    }
}




int
ductkqfilter(dev_t dev, struct knote *kn)
{
    struct duct_softc *sc = duct_lookup(dev);

    if (sc == NULL)
        return (ENXIO);

    switch (kn->kn_filter) {
    case EVFILT_READ:
        kn->kn_fop = &duct_read_filtops;
        break;
    case EVFILT_WRITE:
        kn->kn_fop = &duct_write_filtops;
        break;
    default:
        return (EINVAL);
    }

    kn->kn_hook = sc;
    mtx_enter(&sc->sc_mtx);
    klist_insert(&sc->sc_klist, kn);
    mtx_leave(&sc->sc_mtx);

    return 0;
}

int
duct_read_event(struct knote *kn, long hint)
{
    struct duct_softc *sc = kn->kn_hook;

    MUTEX_ASSERT_LOCKED(&sc->sc_mtx);

    /* Determine whether there is data in the RX queue */
    if (sc->sc_rx_qhead == sc->sc_rx_qtail) {
        kn->kn_data = 0;
        return 0;
    } else {
        /* Counting the number of readable packets */
        u_int available;
        if (sc->sc_rx_qtail >= sc->sc_rx_qhead)
            available = sc->sc_rx_qtail - sc->sc_rx_qhead;
        else
            available = (sc->sc_rx_qsize - sc->sc_rx_qhead) + sc->sc_rx_qtail;
        kn->kn_data = available;
        return 1;
    }
}

int
duct_write_event(struct knote *kn, long hint)
{
    struct duct_softc *sc = kn->kn_hook;

    MUTEX_ASSERT_LOCKED(&sc->sc_mtx);

    /* Determine whether there is a vacancy in the TX ring */
    u_int next_prod = (sc->sc_tx_prod + 1) % sc->sc_tx_size;
    if (next_prod == sc->sc_tx_cons) {
        kn->kn_data = 0;
        return 0;   /* Ring full, cannot be written */
    } else {
        /* Calculate the number of available slots */
        u_int free_slots;
        if (sc->sc_tx_cons > sc->sc_tx_prod)
            free_slots = sc->sc_tx_cons - sc->sc_tx_prod - 1;
        else
            free_slots = (sc->sc_tx_size - sc->sc_tx_prod) + sc->sc_tx_cons - 1;
        kn->kn_data = free_slots;
        return 1;
    }
}

void
duct_kqdetach(struct knote *kn)
{
    struct duct_softc *sc = kn->kn_hook;

    mtx_enter(&sc->sc_mtx);
    klist_remove(&sc->sc_klist, kn);
    mtx_leave(&sc->sc_mtx);
}


int 
duct_filt_process(struct knote *kn, struct kevent *kev)
{
	struct duct_softc *sc = kn->kn_hook;
	int active;
	/* When entered from a syscall we can take the lock */
	mtx_enter(&sc->sc_mtx);
	active = knote_process(kn, kev);
	mtx_leave(&sc->sc_mtx);
	
	return (active);
}

/* ========================= INTERRUPT HANDLERS ======================== */
int
duct_intr_event(void *arg)
{
    struct duct_softc *sc = arg;
    uint32_t evflags;

    /* Read-once (clear-on-read) */
    evflags = bus_space_read_4(sc->sc_iot, sc->sc_ioh, A2_REG_EVFLAGS);
    if (evflags == 0)
        return 1;   /* spurious */

    /* Snapshot important indices for debugging */
    printf("%s: EVFLAGS=0x%08x state=%u "
           "cmd[c=%u p=%u pend=%u] rx[c=%u p=%u] tx[c=%u p=%u]\n",
           sc->sc_dev.dv_xname, evflags, sc->sc_state,
           sc->sc_cmd_cons, sc->sc_cmd_prod, sc->sc_cmd_pending,
           sc->sc_rx_cons,  sc->sc_rx_prod,
           sc->sc_tx_cons,  sc->sc_tx_prod);

    /* TX completions */
    if (evflags & A2_EV_TXCOMP) {
        size_t tx_ring_size = sc->sc_tx_size * sizeof(struct a2_tx_desc);
        bus_dmamap_sync(sc->sc_dmat, sc->sc_tx_map, 0, tx_ring_size,
            BUS_DMASYNC_POSTREAD);
        duct_tx_process(sc);
    }

    /* RX completions */
    if (evflags & A2_EV_RXCOMP) {
        size_t rx_ring_size = sc->sc_rx_size * sizeof(struct a2_rx_desc);
        bus_dmamap_sync(sc->sc_dmat, sc->sc_rx_map, 0, rx_ring_size,
            BUS_DMASYNC_POSTREAD);
        duct_rx_process(sc);
    }

    /* Command completions */
    if (evflags & A2_EV_CMDCOMP) {
        size_t cmd_ring_size = sc->sc_cmd_size * sizeof(struct a2_cmd_desc);
        bus_dmamap_sync(sc->sc_dmat, sc->sc_cmd_map, 0, cmd_ring_size,
            BUS_DMASYNC_POSTREAD);
        mtx_enter(&sc->sc_mtx);
        duct_cmd_process(sc);
        mtx_leave(&sc->sc_mtx);
    }

    if (evflags & A2_EV_RXDROP)
        printf("%s: RXDROP (rx ring likely exhausted)\n", sc->sc_dev.dv_xname);

    if (evflags & A2_EV_RXJUMBO)
        printf("%s: RXJUMBO (packet too large)\n", sc->sc_dev.dv_xname);

    return 1;
}



int
duct_intr_error(void *arg)
{
    struct duct_softc *sc = arg;
    uint32_t flags;

    flags = bus_space_read_4(sc->sc_iot, sc->sc_ioh, A2_REG_FLAGS);

    printf("%s: fatal error interrupt, FLAGS=0x%08x\n",
        sc->sc_dev.dv_xname, flags);

    if (flags & A2_FLAGS_FLTB)
        printf("%s: error FLTB - BAR pointer fault\n", sc->sc_dev.dv_xname);
    if (flags & A2_FLAGS_FLTR)
        printf("%s: error FLTR - descriptor ring pointer fault\n", sc->sc_dev.dv_xname);
    if (flags & A2_FLAGS_SEQ)
        printf("%s: error SEQ - out-of-sequence operation\n", sc->sc_dev.dv_xname);
    if (flags & A2_FLAGS_HWERR)
        printf("%s: error HWERR - miscellaneous hardware error\n", sc->sc_dev.dv_xname);

    /* Enter error state */
    sc->sc_state = DUCT_S_ERROR;

    /* Wake up all blocked syscalls so they can return EIO */
    wakeup(&sc->sc_state);
    wakeup(&sc->sc_cmd_cons);
    wakeup(&sc->sc_tx_queue);
    wakeup(&sc->sc_rx_queue);
    selwakeup(&sc->sc_selinfo);
    knote(&sc->sc_klist, 0);

    printf("%s: device stopped, reset required\n", sc->sc_dev.dv_xname);

    return 1;
}


/* ========================= COMMAND RING FUNCTIONS ==================== */
int
duct_cmd_alloc(struct duct_softc *sc)
{
	int error;
	
	/* Allocate command ring (32 descriptors, each 32 bytes = 1KB) */
	sc->sc_cmd_size = 32;
	size_t cmd_ring_size = sc->sc_cmd_size * sizeof(struct a2_cmd_desc);
	
	/* Allocate DMA memory for command ring */
	int rsegs;
	error = bus_dmamem_alloc(sc->sc_dmat, cmd_ring_size, PAGE_SIZE, 0,
	    &sc->sc_cmd_seg, 1, &rsegs, BUS_DMA_WAITOK | BUS_DMA_ZERO);
	if (error != 0) {
		printf(": failed to allocate command ring memory\n");
		return error;
	}
	
	/* Map command ring to kernel virtual address */
	error = bus_dmamem_map(sc->sc_dmat, &sc->sc_cmd_seg, 1, cmd_ring_size,
	    (caddr_t *)&sc->sc_cmd_kva, BUS_DMA_WAITOK | BUS_DMA_COHERENT);
	if (error != 0) {
		printf(": failed to map command ring memory\n");
		bus_dmamem_free(sc->sc_dmat, &sc->sc_cmd_seg, 1);
		return error;
	}
	
	/* Create DMA map for command ring */
	error = bus_dmamap_create(sc->sc_dmat, cmd_ring_size, 1, cmd_ring_size, 0,
	    BUS_DMA_WAITOK, &sc->sc_cmd_map);
	if (error != 0) {
		printf(": failed to create command ring DMA map\n");
		bus_dmamem_unmap(sc->sc_dmat, sc->sc_cmd_kva, cmd_ring_size);
		bus_dmamem_free(sc->sc_dmat, &sc->sc_cmd_seg, 1);
		return error;
	}
	
	/* Load DMA map */
	error = bus_dmamap_load(sc->sc_dmat, sc->sc_cmd_map, sc->sc_cmd_kva,
	    cmd_ring_size, NULL, BUS_DMA_WAITOK);
	if (error != 0) {
		printf(": failed to load command ring DMA map\n");
		bus_dmamap_destroy(sc->sc_dmat, sc->sc_cmd_map);
		bus_dmamem_unmap(sc->sc_dmat, sc->sc_cmd_kva, cmd_ring_size);
		bus_dmamem_free(sc->sc_dmat, &sc->sc_cmd_seg, 1);
		return error;
	}
	
	sc->sc_cmd_pa = sc->sc_cmd_map->dm_segs[0].ds_addr;
	sc->sc_cmd_prod = sc->sc_cmd_cons = 0;
	sc->sc_cmd_pending = 0;
	
	/* Configure command ring base address and size in device registers */
	bus_space_write_8(sc->sc_iot, sc->sc_ioh, A2_REG_CMDBASE, sc->sc_cmd_pa);
	bus_space_barrier(sc->sc_iot, sc->sc_ioh, A2_REG_CMDBASE, 8,
	    BUS_SPACE_BARRIER_WRITE);
	
	/* Calculate log2 of command ring size for shift register */
	uint32_t cmd_shift = flsl(sc->sc_cmd_size) - 1;
	bus_space_write_4(sc->sc_iot, sc->sc_ioh, A2_REG_CMDSHIFT, cmd_shift);
	bus_space_barrier(sc->sc_iot, sc->sc_ioh, A2_REG_CMDSHIFT, 4,
	    BUS_SPACE_BARRIER_WRITE);
	
	printf(": command ring allocated, size=%u descriptors, pa=0x%lx, shift=%u\n", 
	    sc->sc_cmd_size, sc->sc_cmd_pa, cmd_shift);
	return 0;
}

void
duct_cmd_free(struct duct_softc *sc)
{
	if (sc->sc_cmd_map) {
		bus_dmamap_unload(sc->sc_dmat, sc->sc_cmd_map);
		bus_dmamap_destroy(sc->sc_dmat, sc->sc_cmd_map);
	}
	if (sc->sc_cmd_kva) {
		size_t cmd_ring_size = sc->sc_cmd_size * sizeof(struct a2_cmd_desc);
		bus_dmamem_unmap(sc->sc_dmat, sc->sc_cmd_kva, cmd_ring_size);
		bus_dmamem_free(sc->sc_dmat, &sc->sc_cmd_seg, 1);
	}
}

int
duct_cmd_submit(struct duct_softc *sc, uint32_t cmd, uint32_t mask, uint32_t addr)
{
    struct a2_cmd_desc *desc;
    u_int idx;

    /* Get next descriptor index */
    idx = sc->sc_cmd_prod & (sc->sc_cmd_size - 1);
    desc = (struct a2_cmd_desc *)sc->sc_cmd_kva + idx;

    /* Check if descriptor is still owned by device */
    if (desc->a2cd_owner == A2_OWNER_DEVICE) {
        printf("%s: cmd ring full at idx=%u\n", sc->sc_dev.dv_xname, idx);
        return EBUSY;
    }

    /* Fill descriptor fields */
    desc->a2cd_type     = cmd;
    desc->a2cd_filtmask = mask;
    desc->a2cd_filtaddr = addr;

    /* Ensure all fields visible before ownership change */
    membar_producer();

    /* Give ownership to device */
    desc->a2cd_owner = A2_OWNER_DEVICE;

    /* Sync only this descriptor, not the whole ring */
    bus_dmamap_sync(sc->sc_dmat, sc->sc_cmd_map,
        idx * sizeof(struct a2_cmd_desc),
        sizeof(struct a2_cmd_desc),
        BUS_DMASYNC_PREWRITE);

    /* Advance producer and increment pending */
    sc->sc_cmd_prod++;
    sc->sc_cmd_pending++;

    membar_producer();

    printf("%s: cmd_submit idx=%u cmd=0x%08x mask=0x%08x addr=0x%08x (pending=%u)\n",
        sc->sc_dev.dv_xname, idx, cmd, mask, addr, sc->sc_cmd_pending);

    return 0;
}


void
duct_cmd_process(struct duct_softc *sc)
{
    struct a2_cmd_desc *desc;
    u_int idx;

    while (sc->sc_cmd_cons != sc->sc_cmd_prod) {
        idx = sc->sc_cmd_cons & (sc->sc_cmd_size - 1);
        desc = (struct a2_cmd_desc *)sc->sc_cmd_kva + idx;

        membar_consumer();

        /* Debug print each descriptor we check */
        printf("%s: cmd_process idx=%u owner=0x%02x type=0x%02x err=0x%02x\n",
            sc->sc_dev.dv_xname, idx,
            desc->a2cd_owner, desc->a2cd_type, desc->a2cd_err);

        if (desc->a2cd_owner == A2_OWNER_DEVICE) {
            /* Still owned by device, stop */
            break;
        }

        /* Map device error code to errno */
        switch (desc->a2cd_err) {
        case A2_ERR_OK:
            sc->sc_cmd_errno = 0;
            break;
        case A2_ERR_INVAL:
            sc->sc_cmd_errno = EINVAL;
            break;
        case A2_ERR_NOSPC:
            sc->sc_cmd_errno = ENOSPC;
            break;
        case A2_ERR_NOENT:
            sc->sc_cmd_errno = ENOENT;
            break;
        default:
            sc->sc_cmd_errno = EIO;
            break;
        }

        if (sc->sc_cmd_errno == 0) {
            switch (desc->a2cd_type) {
            case A2_CMD_START:
                sc->sc_state = DUCT_S_RUNNING;
                wakeup(&sc->sc_state);
                printf("%s: START completed\n", sc->sc_dev.dv_xname);
                break;
            case A2_CMD_STOP:
                sc->sc_state = DUCT_S_STOPPED;
                wakeup(&sc->sc_state);
                printf("%s: STOP completed\n", sc->sc_dev.dv_xname);
                break;
            case A2_CMD_ADDFILT:
                printf("%s: ADDFILT completed\n", sc->sc_dev.dv_xname);
                break;
            case A2_CMD_RMFILT:
                printf("%s: RMFILT completed\n", sc->sc_dev.dv_xname);
                break;
            case A2_CMD_FLUSHFILT:
                printf("%s: FLUSHFILT completed\n", sc->sc_dev.dv_xname);
                break;
            default:
                printf("%s: Unknown command completed type=0x%02x\n",
                    sc->sc_dev.dv_xname, desc->a2cd_type);
                break;
            }
        } else {
            printf("%s: command failed type=0x%02x err=0x%02x → errno=%d\n",
                sc->sc_dev.dv_xname, desc->a2cd_type, desc->a2cd_err, sc->sc_cmd_errno);
            wakeup(&sc->sc_state);
        }

        /* Consume descriptor */
        sc->sc_cmd_cons++;
        sc->sc_cmd_pending--;
        wakeup(&sc->sc_cmd_cons);
    }
}



/* ========================= RX RING FUNCTIONS ======================== */

int
duct_rx_alloc(struct duct_softc *sc)
{
	int error;
	int rsegs;
	
	/* Allocate RX ring (64 descriptors, each 16 bytes = 1KB) */
	sc->sc_rx_size = 64;
	size_t rx_ring_size = sc->sc_rx_size * sizeof(struct a2_rx_desc);
	
	/* Allocate DMA memory for RX ring */
	error = bus_dmamem_alloc(sc->sc_dmat, rx_ring_size, PAGE_SIZE, 0,
	    &sc->sc_rx_seg, 1, &rsegs, BUS_DMA_WAITOK | BUS_DMA_ZERO);
	if (error != 0) {
		printf(": failed to allocate RX ring memory\n");
		return error;
	}
	
	/* Map RX ring to kernel virtual address */
	error = bus_dmamem_map(sc->sc_dmat, &sc->sc_rx_seg, 1, rx_ring_size,
	    (caddr_t *)&sc->sc_rx_kva, BUS_DMA_WAITOK | BUS_DMA_COHERENT);
	if (error != 0) {
		printf(": failed to map RX ring memory\n");
		bus_dmamem_free(sc->sc_dmat, &sc->sc_rx_seg, 1);
		return error;
	}
	
	/* Get physical address */
	sc->sc_rx_pa = sc->sc_rx_seg.ds_addr;
	
	/* Create DMA map for RX ring */
	error = bus_dmamap_create(sc->sc_dmat, rx_ring_size, 1, rx_ring_size, 0,
	    BUS_DMA_WAITOK, &sc->sc_rx_map);
	if (error != 0) {
		printf(": failed to create RX ring DMA map\n");
		bus_dmamem_unmap(sc->sc_dmat, sc->sc_rx_kva, rx_ring_size);
		bus_dmamem_free(sc->sc_dmat, &sc->sc_rx_seg, 1);
		return error;
	}
	
	/* Load DMA map */
	error = bus_dmamap_load(sc->sc_dmat, sc->sc_rx_map, sc->sc_rx_kva,
	    rx_ring_size, NULL, BUS_DMA_WAITOK);
	if (error != 0) {
		printf(": failed to load RX ring DMA map\n");
		bus_dmamap_destroy(sc->sc_dmat, sc->sc_rx_map);
		bus_dmamem_unmap(sc->sc_dmat, sc->sc_rx_kva, rx_ring_size);
		bus_dmamem_free(sc->sc_dmat, &sc->sc_rx_seg, 1);
		return error;
	}
	
	/* Allocate RX buffers (64 buffers, each 2048 bytes) */
	sc->sc_rx_buf_size = 2048;
	sc->sc_rx_buf_maps = mallocarray(sc->sc_rx_size, sizeof(bus_dmamap_t),
	    M_DEVBUF, M_WAITOK | M_ZERO);
	sc->sc_rx_buf_kva = mallocarray(sc->sc_rx_size, sizeof(void *),
	    M_DEVBUF, M_WAITOK | M_ZERO);
	sc->sc_rx_buf_pa = mallocarray(sc->sc_rx_size, sizeof(paddr_t),
	    M_DEVBUF, M_WAITOK | M_ZERO);
	sc->sc_rx_buf_segs = mallocarray(sc->sc_rx_size, sizeof(bus_dma_segment_t),
	    M_DEVBUF, M_WAITOK | M_ZERO);
	
	/* Allocate individual RX buffers and initialize descriptors */
	for (int i = 0; i < sc->sc_rx_size; i++) {
		/* Allocate DMA memory for RX buffer */
		error = bus_dmamem_alloc(sc->sc_dmat, sc->sc_rx_buf_size, PAGE_SIZE, 0,
		    &sc->sc_rx_buf_segs[i], 1, &rsegs, BUS_DMA_WAITOK | BUS_DMA_ZERO);
		if (error != 0) {
			printf(": failed to allocate RX buffer %d\n", i);
			/* Cleanup already allocated buffers */
			for (int j = 0; j < i; j++) {
				bus_dmamem_free(sc->sc_dmat, &sc->sc_rx_buf_segs[j], 1);
			}
			goto cleanup_rx_buf_arrays;
		}
		
		/* Map RX buffer to kernel virtual address */
		error = bus_dmamem_map(sc->sc_dmat, &sc->sc_rx_buf_segs[i], 1, sc->sc_rx_buf_size,
		    (caddr_t *)&sc->sc_rx_buf_kva[i], BUS_DMA_WAITOK | BUS_DMA_COHERENT);
		if (error != 0) {
			printf(": failed to map RX buffer %d\n", i);
			bus_dmamem_free(sc->sc_dmat, &sc->sc_rx_buf_segs[i], 1);
			/* Cleanup already allocated buffers */
			for (int j = 0; j < i; j++) {
				bus_dmamem_free(sc->sc_dmat, &sc->sc_rx_buf_segs[j], 1);
			}
			goto cleanup_rx_buf_arrays;
		}
		
		/* Get physical address */
		sc->sc_rx_buf_pa[i] = sc->sc_rx_buf_segs[i].ds_addr;
		
		/* Create DMA map for RX buffer */
		error = bus_dmamap_create(sc->sc_dmat, sc->sc_rx_buf_size, 1, sc->sc_rx_buf_size, 0,
		    BUS_DMA_WAITOK, &sc->sc_rx_buf_maps[i]);
		if (error != 0) {
			printf(": failed to create RX buffer %d DMA map\n", i);
			bus_dmamem_unmap(sc->sc_dmat, sc->sc_rx_buf_kva[i], sc->sc_rx_buf_size);
			bus_dmamem_free(sc->sc_dmat, &sc->sc_rx_buf_segs[i], 1);
			/* Cleanup already allocated buffers */
			for (int j = 0; j < i; j++) {
				bus_dmamem_free(sc->sc_dmat, &sc->sc_rx_buf_segs[j], 1);
			}
			goto cleanup_rx_buf_arrays;
		}
		
		/* Load DMA map */
		error = bus_dmamap_load(sc->sc_dmat, sc->sc_rx_buf_maps[i], sc->sc_rx_buf_kva[i],
		    sc->sc_rx_buf_size, NULL, BUS_DMA_WAITOK);
		if (error != 0) {
			printf(": failed to load RX buffer %d DMA map\n", i);
			bus_dmamap_destroy(sc->sc_dmat, sc->sc_rx_buf_maps[i]);
			bus_dmamem_unmap(sc->sc_dmat, sc->sc_rx_buf_kva[i], sc->sc_rx_buf_size);
			bus_dmamem_free(sc->sc_dmat, &sc->sc_rx_buf_segs[i], 1);
			/* Cleanup already allocated buffers */
			for (int j = 0; j < i; j++) {
				bus_dmamem_free(sc->sc_dmat, &sc->sc_rx_buf_segs[j], 1);
			}
			goto cleanup_rx_buf_arrays;
		}
		
		/* Initialize RX descriptor */
		struct a2_rx_desc *desc = (struct a2_rx_desc *)sc->sc_rx_kva + i;
		desc->a2rd_ptr[0] = sc->sc_rx_buf_pa[i];
		desc->a2rd_length[0] = sc->sc_rx_buf_size;
		desc->a2rd_length[1] = 0;
		desc->a2rd_length[2] = 0;
		desc->a2rd_length[3] = 0;
		desc->a2rd_owner = A2_OWNER_DEVICE;  /* Give ownership to device */
		
		/* Sync RX buffer to ensure device can see initial state */
		bus_dmamap_sync(sc->sc_dmat, sc->sc_rx_buf_maps[i], 0, 
		    sc->sc_rx_buf_size, BUS_DMASYNC_PREREAD);
	}
	
	/* Initialize RX ring indices */
	sc->sc_rx_prod = sc->sc_rx_size;  /* All buffers given to device */
	sc->sc_rx_cons = 0;
	
	/* Configure RX ring base address and size in device registers */
	bus_space_write_8(sc->sc_iot, sc->sc_ioh, A2_REG_RXBASE, sc->sc_rx_pa);
	bus_space_barrier(sc->sc_iot, sc->sc_ioh, A2_REG_RXBASE, 8,
	    BUS_SPACE_BARRIER_WRITE);
	
	uint32_t rx_shift = flsl(sc->sc_rx_size) - 1;
	bus_space_write_4(sc->sc_iot, sc->sc_ioh, A2_REG_RXSHIFT, rx_shift);
	bus_space_barrier(sc->sc_iot, sc->sc_ioh, A2_REG_RXSHIFT, 4,
	    BUS_SPACE_BARRIER_WRITE);
	
	/* Sync RX ring to ensure device can see initial state */
	bus_dmamap_sync(sc->sc_dmat, sc->sc_rx_map, 0, rx_ring_size, BUS_DMASYNC_PREREAD);
	
	printf(": RX ring allocated: %d descriptors, %d buffers, pa=0x%lx, shift=%u\n", 
	    sc->sc_rx_size, sc->sc_rx_size, sc->sc_rx_pa, rx_shift);
	
	return 0;

cleanup_rx_buf_arrays:
	/* Free RX buffer arrays */
	if (sc->sc_rx_buf_maps) {
		free(sc->sc_rx_buf_maps, M_DEVBUF, sc->sc_rx_size * sizeof(bus_dmamap_t));
		sc->sc_rx_buf_maps = NULL;
	}
	if (sc->sc_rx_buf_kva) {
		free(sc->sc_rx_buf_kva, M_DEVBUF, sc->sc_rx_size * sizeof(void *));
		sc->sc_rx_buf_kva = NULL;
	}
	if (sc->sc_rx_buf_pa) {
		free(sc->sc_rx_buf_pa, M_DEVBUF, sc->sc_rx_size * sizeof(paddr_t));
		sc->sc_rx_buf_pa = NULL;
	}
	if (sc->sc_rx_buf_segs) {
		free(sc->sc_rx_buf_segs, M_DEVBUF, sc->sc_rx_size * sizeof(bus_dma_segment_t));
		sc->sc_rx_buf_segs = NULL;
	}
	
	/* Free RX ring */
	if (sc->sc_rx_map) {
		bus_dmamap_unload(sc->sc_dmat, sc->sc_rx_map);
		bus_dmamap_destroy(sc->sc_dmat, sc->sc_rx_map);
		sc->sc_rx_map = NULL;
	}
	if (sc->sc_rx_kva) {
		size_t rx_ring_size = sc->sc_rx_size * sizeof(struct a2_rx_desc);
		bus_dmamem_unmap(sc->sc_dmat, sc->sc_rx_kva, rx_ring_size);
		sc->sc_rx_kva = NULL;
	}
	if (sc->sc_rx_seg.ds_addr) {
		bus_dmamem_free(sc->sc_dmat, &sc->sc_rx_seg, 1);
		sc->sc_rx_seg.ds_addr = 0;
	}
	
	return error;
}

void
duct_rx_free(struct duct_softc *sc)
{
	int i;
	
	/* Free RX buffers */
	if (sc->sc_rx_buf_maps) {
		for (i = 0; i < sc->sc_rx_size; i++) {
			if (sc->sc_rx_buf_maps[i]) {
				bus_dmamap_destroy(sc->sc_dmat, sc->sc_rx_buf_maps[i]);
			}
		}
		free(sc->sc_rx_buf_maps, M_DEVBUF, sc->sc_rx_size * sizeof(bus_dmamap_t));
		sc->sc_rx_buf_maps = NULL;
	}
	
	if (sc->sc_rx_buf_segs) {
		for (i = 0; i < sc->sc_rx_size; i++) {
			if (sc->sc_rx_buf_segs[i].ds_addr) {
				bus_dmamem_free(sc->sc_dmat, &sc->sc_rx_buf_segs[i], 1);
			}
		}
		free(sc->sc_rx_buf_segs, M_DEVBUF, sc->sc_rx_size * sizeof(bus_dma_segment_t));
		sc->sc_rx_buf_segs = NULL;
	}
	
	if (sc->sc_rx_buf_kva) {
		free(sc->sc_rx_buf_kva, M_DEVBUF, sc->sc_rx_size * sizeof(void *));
		sc->sc_rx_buf_kva = NULL;
	}
	
	if (sc->sc_rx_buf_pa) {
		free(sc->sc_rx_buf_pa, M_DEVBUF, sc->sc_rx_size * sizeof(paddr_t));
		sc->sc_rx_buf_pa = NULL;
	}
	
	/* Free RX ring */
	if (sc->sc_rx_map) {
		bus_dmamap_unload(sc->sc_dmat, sc->sc_rx_map);
		bus_dmamap_destroy(sc->sc_dmat, sc->sc_rx_map);
		sc->sc_rx_map = NULL;
	}
	
	if (sc->sc_rx_kva) {
		size_t rx_ring_size = sc->sc_rx_size * sizeof(struct a2_rx_desc);
		bus_dmamem_unmap(sc->sc_dmat, sc->sc_rx_kva, rx_ring_size);
		sc->sc_rx_kva = NULL;
	}
	
	if (sc->sc_rx_seg.ds_addr) {
		bus_dmamem_free(sc->sc_dmat, &sc->sc_rx_seg, 1);
		sc->sc_rx_seg.ds_addr = 0;
	}
	
	printf(": RX ring freed\n");
}

void
duct_rx_process(struct duct_softc *sc)
{
    struct a2_rx_desc *desc;
    struct duct_packet_hdr *pkt_hdr;
    u_int idx;

    while (sc->sc_rx_cons != sc->sc_rx_prod) {
        idx = sc->sc_rx_cons & (sc->sc_rx_size - 1);
        desc = (struct a2_rx_desc *)sc->sc_rx_kva + idx;

        membar_consumer();

        if (desc->a2rd_owner == A2_OWNER_DEVICE) {
            /* Device still owns this descriptor */
            break;
        }

        /* Debug: show descriptor status */
        printf("%s: RX idx=%u owner=%02x pktlen=%u len0=%u\n",
            sc->sc_dev.dv_xname, idx,
            desc->a2rd_owner, desc->a2rd_pktlen, desc->a2rd_length[0]);

        /* Sync RX buffer so CPU sees device-written data */
        bus_dmamap_sync(sc->sc_dmat, sc->sc_rx_buf_maps[idx], 0,
            MIN(desc->a2rd_pktlen, sc->sc_rx_buf_size), BUS_DMASYNC_POSTREAD);

        pkt_hdr = (struct duct_packet_hdr *)sc->sc_rx_buf_kva[idx];

        /* Case 1: packet shorter than header */
        if (desc->a2rd_pktlen < sizeof(struct duct_packet_hdr)) {
            printf("%s: RX short packet: %u < %zu\n",
                sc->sc_dev.dv_xname, desc->a2rd_pktlen, sizeof(struct duct_packet_hdr));
            goto recycle;
        }

        /* Case 2: payload length mismatch */
        if (pkt_hdr->dpkt_length > 0 &&
            desc->a2rd_pktlen < sizeof(struct duct_packet_hdr) + pkt_hdr->dpkt_length) {
            printf("%s: RX payload mismatch: pktlen=%u hdr_len=%zu payload=%u\n",
                sc->sc_dev.dv_xname, desc->a2rd_pktlen,
                sizeof(struct duct_packet_hdr), pkt_hdr->dpkt_length);
            goto recycle;
        }

        /* Case 3: valid packet → enqueue */
        u_int next_tail = (sc->sc_rx_qtail + 1) & (sc->sc_rx_qsize - 1);
        mtx_enter(&sc->sc_mtx);
        if (next_tail != sc->sc_rx_qhead) {
            sc->sc_rx_queue[sc->sc_rx_qtail] = *pkt_hdr;
            if (pkt_hdr->dpkt_length > 0) {
                sc->sc_rx_payload[sc->sc_rx_qtail] = malloc(pkt_hdr->dpkt_length,
                    M_DEVBUF, M_WAITOK);
                if (sc->sc_rx_payload[sc->sc_rx_qtail] != NULL) {
                    memcpy(sc->sc_rx_payload[sc->sc_rx_qtail],
                        (char *)sc->sc_rx_buf_kva[idx] + sizeof(struct duct_packet_hdr),
                        pkt_hdr->dpkt_length);
                    sc->sc_rx_payload_len[sc->sc_rx_qtail] = pkt_hdr->dpkt_length;
                } else {
                    sc->sc_rx_payload[sc->sc_rx_qtail] = NULL;
                    sc->sc_rx_payload_len[sc->sc_rx_qtail] = 0;
                }
            } else {
                sc->sc_rx_payload[sc->sc_rx_qtail] = NULL;
                sc->sc_rx_payload_len[sc->sc_rx_qtail] = 0;
            }
            sc->sc_rx_qtail = next_tail;

            printf("%s: RX queued idx=%u src=0x%08x dst=0x%08x len=%u\n",
                sc->sc_dev.dv_xname, idx,
                pkt_hdr->dpkt_source, pkt_hdr->dpkt_destination, pkt_hdr->dpkt_length);

            wakeup(&sc->sc_rx_queue);
            selwakeup(&sc->sc_selinfo);
            knote(&sc->sc_klist, 0);
        } else {
            printf("%s: RX queue full, dropping packet idx=%u\n",
                sc->sc_dev.dv_xname, idx);
        }
        mtx_leave(&sc->sc_mtx);

recycle:
        /* Recycle descriptor for device use */
        bus_dmamap_sync(sc->sc_dmat, sc->sc_rx_buf_maps[idx], 0,
            sc->sc_rx_buf_size, BUS_DMASYNC_PREREAD);

        membar_producer();
        bus_dmamap_sync(sc->sc_dmat, sc->sc_rx_map,
            idx * sizeof(struct a2_rx_desc),
            sizeof(struct a2_rx_desc), BUS_DMASYNC_PREWRITE);

        desc->a2rd_owner = A2_OWNER_DEVICE;
        sc->sc_rx_cons = (sc->sc_rx_cons + 1) % sc->sc_rx_size;
        sc->sc_rx_prod = (sc->sc_rx_prod + 1) % sc->sc_rx_size;

        printf("%s: RX recycled idx=%u owner->DEVICE\n",
            sc->sc_dev.dv_xname, idx);
    }
}



/* ========================= TX RING FUNCTIONS ========================= */

/*
 * Allocate TX ring and buffers
 */
int
duct_tx_alloc(struct duct_softc *sc)
{
	int error;
	size_t tx_ring_size;
	u_int i = 0;
	
	/* Allocate TX ring (64 descriptors) */
	sc->sc_tx_size = 64;
	tx_ring_size = sc->sc_tx_size * sizeof(struct a2_tx_desc);
	
	/* Step 1: Allocate DMA memory */
	int rsegs;
	error = bus_dmamem_alloc(sc->sc_dmat, tx_ring_size, PAGE_SIZE, 0,
	    &sc->sc_tx_seg, 1, &rsegs, BUS_DMA_WAITOK | BUS_DMA_ZERO);
	if (error != 0) {
		printf(": failed to allocate TX ring DMA memory: %d\n", error);
		return error;
	}
	
	/* Step 2: Map DMA memory */
	error = bus_dmamem_map(sc->sc_dmat, &sc->sc_tx_seg, 1, tx_ring_size,
	    (caddr_t *)&sc->sc_tx_kva, BUS_DMA_WAITOK);
	if (error != 0) {
		printf(": failed to map TX ring: %d\n", error);
		bus_dmamem_free(sc->sc_dmat, &sc->sc_tx_seg, 1);
		return error;
	}
	
	/* Step 3: Create DMA map */
	error = bus_dmamap_create(sc->sc_dmat, tx_ring_size, 1, tx_ring_size, 0,
	    BUS_DMA_WAITOK | BUS_DMA_ALLOCNOW, &sc->sc_tx_map);
	if (error != 0) {
		printf(": failed to create TX ring DMA map: %d\n", error);
		bus_dmamem_unmap(sc->sc_dmat, sc->sc_tx_kva, tx_ring_size);
		bus_dmamem_free(sc->sc_dmat, &sc->sc_tx_seg, 1);
		return error;
	}
	
	/* Step 4: Load DMA map */
	error = bus_dmamap_load(sc->sc_dmat, sc->sc_tx_map, sc->sc_tx_kva,
	    tx_ring_size, NULL, BUS_DMA_WAITOK);
	if (error != 0) {
		printf(": failed to load TX ring DMA map: %d\n", error);
		bus_dmamap_destroy(sc->sc_dmat, sc->sc_tx_map);
		bus_dmamem_unmap(sc->sc_dmat, sc->sc_tx_kva, tx_ring_size);
		bus_dmamem_free(sc->sc_dmat, &sc->sc_tx_seg, 1);
		return error;
	}
	
	sc->sc_tx_pa = sc->sc_tx_map->dm_segs[0].ds_addr;
	sc->sc_tx_prod = sc->sc_tx_cons = 0;
	
	/* Allocate TX buffers */
	sc->sc_tx_buf_size = 2048; /* 2KB per buffer */
	sc->sc_tx_buf_maps = malloc(sc->sc_tx_size * sizeof(bus_dmamap_t),
	    M_DEVBUF, M_WAITOK | M_ZERO);
	sc->sc_tx_buf_kva = malloc(sc->sc_tx_size * sizeof(void *),
	    M_DEVBUF, M_WAITOK | M_ZERO);
	sc->sc_tx_buf_pa = malloc(sc->sc_tx_size * sizeof(paddr_t),
	    M_DEVBUF, M_WAITOK | M_ZERO);
	sc->sc_tx_buf_segs = malloc(sc->sc_tx_size * sizeof(bus_dma_segment_t),
	    M_DEVBUF, M_WAITOK | M_ZERO);
	
	/* Allocate individual TX buffers using 4-step process */
	for (u_int i = 0; i < sc->sc_tx_size; i++) {
		/* Step 1: Allocate DMA memory */
		int buf_rsegs;
		error = bus_dmamem_alloc(sc->sc_dmat, sc->sc_tx_buf_size, PAGE_SIZE, 0,
		    &sc->sc_tx_buf_segs[i], 1, &buf_rsegs, BUS_DMA_WAITOK | BUS_DMA_ZERO);
		if (error != 0) {
			printf(": failed to allocate TX buffer %u: %d\n", i, error);
			goto destroy_tx_ring;
		}
		
		/* Step 2: Map DMA memory */
		error = bus_dmamem_map(sc->sc_dmat, &sc->sc_tx_buf_segs[i], 1,
		    sc->sc_tx_buf_size, (caddr_t *)&sc->sc_tx_buf_kva[i], BUS_DMA_WAITOK);
		if (error != 0) {
			printf(": failed to map TX buffer %u: %d\n", i, error);
			bus_dmamem_free(sc->sc_dmat, &sc->sc_tx_buf_segs[i], 1);
			goto destroy_tx_ring;
		}
		
		/* Step 3: Create DMA map */
		error = bus_dmamap_create(sc->sc_dmat, sc->sc_tx_buf_size, 1, sc->sc_tx_buf_size, 0,
		    BUS_DMA_WAITOK | BUS_DMA_ALLOCNOW, &sc->sc_tx_buf_maps[i]);
		if (error != 0) {
			printf(": failed to create TX buffer %u DMA map: %d\n", i, error);
			bus_dmamem_unmap(sc->sc_dmat, sc->sc_tx_buf_kva[i], sc->sc_tx_buf_size);
			bus_dmamem_free(sc->sc_dmat, &sc->sc_tx_buf_segs[i], 1);
			goto destroy_tx_ring;
		}
		
		/* Step 4: Load DMA map */
		error = bus_dmamap_load(sc->sc_dmat, sc->sc_tx_buf_maps[i], sc->sc_tx_buf_kva[i],
		    sc->sc_tx_buf_size, NULL, BUS_DMA_WAITOK);
		if (error != 0) {
			printf(": failed to load TX buffer %u DMA map: %d\n", i, error);
			bus_dmamap_destroy(sc->sc_dmat, sc->sc_tx_buf_maps[i]);
			bus_dmamem_unmap(sc->sc_dmat, sc->sc_tx_buf_kva[i], sc->sc_tx_buf_size);
			bus_dmamem_free(sc->sc_dmat, &sc->sc_tx_buf_segs[i], 1);
			goto destroy_tx_ring;
		}
		
		sc->sc_tx_buf_pa[i] = sc->sc_tx_buf_maps[i]->dm_segs[0].ds_addr;
		
		/* Initialize TX descriptor */
		struct a2_tx_desc *desc = (struct a2_tx_desc *)sc->sc_tx_kva + i;
		desc->a2td_owner = A2_OWNER_HOST; /* owned by host initially */
		desc->a2td_pktlen = 0;
		desc->a2td_ptr[0] = sc->sc_tx_buf_pa[i];
		desc->a2td_length[0] = 0;
		desc->a2td_length[1] = 0;
		desc->a2td_length[2] = 0;
		desc->a2td_length[3] = 0;
	}
	
	/* Configure TX ring base address and size in device registers */
	bus_space_write_8(sc->sc_iot, sc->sc_ioh, A2_REG_TXBASE, sc->sc_tx_pa);
	bus_space_barrier(sc->sc_iot, sc->sc_ioh, A2_REG_TXBASE, 8,
	    BUS_SPACE_BARRIER_WRITE);
	
	uint32_t tx_shift = flsl(sc->sc_tx_size) - 1;
	bus_space_write_4(sc->sc_iot, sc->sc_ioh, A2_REG_TXSHIFT, tx_shift);
	bus_space_barrier(sc->sc_iot, sc->sc_ioh, A2_REG_TXSHIFT, 4,
	    BUS_SPACE_BARRIER_WRITE);
	
	/* Sync TX ring to ensure device can see initial state */
	bus_dmamap_sync(sc->sc_dmat, sc->sc_tx_map, 0, 
	    sc->sc_tx_size * sizeof(struct a2_tx_desc), BUS_DMASYNC_PREWRITE);
	
	printf(": TX ring allocated: %u descriptors, %u buffers, pa=0x%lx, shift=%u\n", 
	    sc->sc_tx_size, sc->sc_tx_size, sc->sc_tx_pa, tx_shift);
	return 0;

destroy_tx_ring:
	/* Clean up previously allocated TX buffers */
	for (u_int j = 0; j < i; j++) {
		if (sc->sc_tx_buf_maps[j]) {
			bus_dmamap_destroy(sc->sc_dmat, sc->sc_tx_buf_maps[j]);
		}
		if (sc->sc_tx_buf_kva[j]) {
			bus_dmamem_unmap(sc->sc_dmat, sc->sc_tx_buf_kva[j], sc->sc_tx_buf_size);
		}
		if (sc->sc_tx_buf_segs[j].ds_addr) {
			bus_dmamem_free(sc->sc_dmat, &sc->sc_tx_buf_segs[j], 1);
		}
	}
	free(sc->sc_tx_buf_maps, M_DEVBUF, sc->sc_tx_size * sizeof(bus_dmamap_t));
	free(sc->sc_tx_buf_kva, M_DEVBUF, sc->sc_tx_size * sizeof(void *));
	free(sc->sc_tx_buf_pa, M_DEVBUF, sc->sc_tx_size * sizeof(paddr_t));
	free(sc->sc_tx_buf_segs, M_DEVBUF, sc->sc_tx_size * sizeof(bus_dma_segment_t));
	
	/* Clean up TX ring */
	if (sc->sc_tx_map) {
		bus_dmamap_destroy(sc->sc_dmat, sc->sc_tx_map);
	}
	if (sc->sc_tx_kva) {
		bus_dmamem_unmap(sc->sc_dmat, sc->sc_tx_kva, tx_ring_size);
	}
	if (sc->sc_tx_seg.ds_addr) {
		bus_dmamem_free(sc->sc_dmat, &sc->sc_tx_seg, 1);
	}
	return error;
}

/*
 * Free TX ring and buffers
 */
void
duct_tx_free(struct duct_softc *sc)
{
	if (sc->sc_tx_buf_maps) {
		for (u_int i = 0; i < sc->sc_tx_size; i++) {
			if (sc->sc_tx_buf_maps[i]) {
				bus_dmamap_destroy(sc->sc_dmat, sc->sc_tx_buf_maps[i]);
				sc->sc_tx_buf_maps[i] = NULL;
			}
			if (sc->sc_tx_buf_kva[i]) {
				bus_dmamem_unmap(sc->sc_dmat, sc->sc_tx_buf_kva[i], sc->sc_tx_buf_size);
				sc->sc_tx_buf_kva[i] = NULL;
			}
			if (sc->sc_tx_buf_segs[i].ds_addr) {
				bus_dmamem_free(sc->sc_dmat, &sc->sc_tx_buf_segs[i], 1);
				sc->sc_tx_buf_segs[i].ds_addr = 0;
			}
		}
		free(sc->sc_tx_buf_maps, M_DEVBUF, sc->sc_tx_size * sizeof(bus_dmamap_t));
		free(sc->sc_tx_buf_kva, M_DEVBUF, sc->sc_tx_size * sizeof(void *));
		free(sc->sc_tx_buf_pa, M_DEVBUF, sc->sc_tx_size * sizeof(paddr_t));
		free(sc->sc_tx_buf_segs, M_DEVBUF, sc->sc_tx_size * sizeof(bus_dma_segment_t));
		sc->sc_tx_buf_maps = NULL;
		sc->sc_tx_buf_kva = NULL;
		sc->sc_tx_buf_pa = NULL;
		sc->sc_tx_buf_segs = NULL;
	}
	
	if (sc->sc_tx_map) {
		bus_dmamap_destroy(sc->sc_dmat, sc->sc_tx_map);
		sc->sc_tx_map = NULL;
	}
	if (sc->sc_tx_kva) {
		size_t tx_ring_size = sc->sc_tx_size * sizeof(struct a2_tx_desc);
		bus_dmamem_unmap(sc->sc_dmat, sc->sc_tx_kva, tx_ring_size);
		sc->sc_tx_kva = NULL;
	}
	if (sc->sc_tx_seg.ds_addr) {
		bus_dmamem_free(sc->sc_dmat, &sc->sc_tx_seg, 1);
		sc->sc_tx_seg.ds_addr = 0;
	}
	
	printf(": TX ring freed\n");
}

/*
 * Submit packet for transmission
 */
int
duct_tx_submit(struct duct_softc *sc, const void *data, size_t len)
{
	struct a2_tx_desc *desc;
	u_int next_prod;
	
	/* Check if TX ring is full */
	next_prod = (sc->sc_tx_prod + 1) % sc->sc_tx_size;
	if (next_prod == sc->sc_tx_cons) {
		printf(": TX ring full\n");
		return (ENOBUFS);
	}
	
	/* Check packet size */
	if (len > sc->sc_tx_buf_size) {
		printf(": packet too large: %zu > %u\n", len, sc->sc_tx_buf_size);
		return (EMSGSIZE);
	}
	
	/* Get TX descriptor */
	desc = (struct a2_tx_desc *)sc->sc_tx_kva + sc->sc_tx_prod;
	
	/* Copy data to TX buffer */
	memcpy(sc->sc_tx_buf_kva[sc->sc_tx_prod], data, len);
	
	/* Sync DMA buffer before giving to device */
	bus_dmamap_sync(sc->sc_dmat, sc->sc_tx_buf_maps[sc->sc_tx_prod],
	    0, len, BUS_DMASYNC_PREWRITE);
	
	/* Update descriptor fields */
	desc->a2td_pktlen     = len;
	desc->a2td_length[0]  = len;
	desc->a2td_ptr[0]     = sc->sc_tx_buf_pa[sc->sc_tx_prod];

	/* Give ownership to device: write owner after fields */
	membar_producer();                 /* ensure fields visible before owner */
	desc->a2td_owner = A2_OWNER_DEVICE;

	/* Ensure the descriptor itself is visible to the device (ring PREWRITE) */
	bus_dmamap_sync(sc->sc_dmat, sc->sc_tx_map,
    	sc->sc_tx_prod * sizeof(struct a2_tx_desc),
    	sizeof(struct a2_tx_desc), BUS_DMASYNC_PREWRITE);

	/* Producer moves only after descriptor is visible */
	membar_producer();
	sc->sc_tx_prod = next_prod;

	/* Ring doorbell for TX (high bit must be set per spec) */
	uint32_t idx = (sc->sc_tx_prod - 1) & (sc->sc_tx_size - 1);
	uint32_t doorbell_val = 0x80000000U | idx;
	bus_space_write_4(sc->sc_iot, sc->sc_ioh, A2_REG_DBELL, doorbell_val);
	bus_space_barrier(sc->sc_iot, sc->sc_ioh, A2_REG_DBELL, 4, BUS_SPACE_BARRIER_WRITE);

	printf(": TX doorbell rung: idx=%d, value=0x%08x\n", idx, doorbell_val);
	
	printf(": TX packet submitted: len=%zu, prod=%u\n", len, sc->sc_tx_prod);
	return 0;
}

void
duct_tx_process(struct duct_softc *sc)
{
    struct a2_tx_desc *desc;
    u_int processed = 0;

    while (sc->sc_tx_cons != sc->sc_tx_prod) {
        desc = (struct a2_tx_desc *)sc->sc_tx_kva + sc->sc_tx_cons;

        /* Ensure descriptor fields coherent before checking owner */
        membar_consumer();

        if (desc->a2td_owner == A2_OWNER_DEVICE) {
            /* Device still owns this descriptor */
            break;
        }

        /* TX completed: sync buffer after device writeback */
        bus_dmamap_sync(sc->sc_dmat, sc->sc_tx_buf_maps[sc->sc_tx_cons],
            0, desc->a2td_pktlen, BUS_DMASYNC_POSTWRITE);

        printf(": TX completed: len=%u\n", desc->a2td_pktlen);

        /* Return ownership to host */
        desc->a2td_owner = A2_OWNER_HOST;
        desc->a2td_pktlen = 0;

        /* Advance consumer index */
        sc->sc_tx_cons = (sc->sc_tx_cons + 1) % sc->sc_tx_size;
        processed++;
    }

    if (processed > 0) {
        printf(": processed %u TX completions\n", processed);

        /* Wake up writers waiting on space */
        wakeup(&sc->sc_tx_queue);
        selwakeup(&sc->sc_selinfo);
        knote(&sc->sc_klist, 0);   /* notify EVFILT_WRITE */
    }
}


/* ========================= RING REINITIALIZATION ======================== */

static void
ring_reinit_rx(struct duct_softc *sc)
{
	struct a2_rx_desc *d;
	u_int i;
	
	printf(": reinitializing RX ring\n");
	
	/* Reset all RX descriptors to initial state */
	for (i = 0; i < sc->sc_rx_size; i++) {
		d = (struct a2_rx_desc *)sc->sc_rx_kva + i;
		d->a2rd_ptr[0] = sc->sc_rx_buf_pa[i];
		d->a2rd_length[0] = sc->sc_rx_buf_size;
		d->a2rd_length[1] = 0;
		d->a2rd_length[2] = 0;
		d->a2rd_length[3] = 0;
		d->a2rd_owner = A2_OWNER_DEVICE;
	}
	
	/* Sync RX ring for device access */
	bus_dmamap_sync(sc->sc_dmat, sc->sc_rx_map, 0, 
	    sc->sc_rx_size * sizeof(struct a2_rx_desc), BUS_DMASYNC_PREREAD);
	
	/* Reset RX ring indices */
	sc->sc_rx_cons = 0;
	sc->sc_rx_prod = sc->sc_rx_size;
}

static void
ring_reinit_tx(struct duct_softc *sc)
{
	struct a2_tx_desc *d;
	u_int i;
	
	printf(": reinitializing TX ring\n");
	
	/* Reset all TX descriptors to initial state */
	for (i = 0; i < sc->sc_tx_size; i++) {
		d = (struct a2_tx_desc *)sc->sc_tx_kva + i;
		d->a2td_owner = A2_OWNER_HOST;
		d->a2td_pktlen = 0;
	}
	
	/* Sync TX ring for device access */
	bus_dmamap_sync(sc->sc_dmat, sc->sc_tx_map, 0, 
	    sc->sc_tx_size * sizeof(struct a2_tx_desc), BUS_DMASYNC_PREWRITE);
	
	/* Reset TX ring indices */
	sc->sc_tx_prod = 0;
	sc->sc_tx_cons = 0;
}



