#include <sys/param.h>
#include <sys/systm.h>
#include <sys/errno.h>
#include <sys/ioctl.h>
#include <sys/fcntl.h>
#include <sys/device.h>
#include <sys/vnode.h>
#include <sys/atomic.h>
#include <sys/event.h>

#include <machine/bus.h>

#include <dev/pci/pcireg.h>
#include <dev/pci/pcivar.h>
#include <dev/pci/pcidevs.h>

#include <dev/pci/p6statsvar.h>

#define P6_BAR            PCI_MAPREG_START /* BAR 0 */

#define P6_R_IBASE        0x00
#define P6_R_ICOUNT       0x08
#define P6_R_OBASE        0x10
#define P6_R_DBELL        0x18
#define P6_R_LEN          0x20


#define P6_S_READY        0
#define P6_S_BUSY         1
#define P6_S_DONE         2
#define P6_S_ERROR        3

struct p6stats_softc {
    struct device         sc_dev;

    pci_chipset_tag_t     sc_pc;
    pci_intr_handle_t     sc_ih;
    void            *sc_ihc;
    pcitag_t         sc_tag;

    bus_dma_tag_t         sc_dmat;
    bus_space_tag_t       sc_memt;
    bus_space_handle_t    sc_memh;
    bus_size_t            sc_mems;

    bus_dmamap_t         sc_dmap_i;
    bus_dmamap_t         sc_dmap_o;

    struct p6stats_output *sc_result;
    bus_dma_segment_t     sc_result_segs[1];
    int                   sc_result_nsegs;

    /* Our list of events defined here */
    struct klist          sc_klist;

    struct mutex          sc_mtx;
    unsigned int          sc_state;
};

static int    p6stats_match(struct device *, void *, void *);
static void   p6stats_attach(struct device *, struct device *, void *);

static int    p6stats_intr(void *);

const struct cfattach p6stats_ca = {
    .ca_devsize    = sizeof(struct p6stats_softc),
    .ca_match      = p6stats_match,
    .ca_attach     = p6stats_attach
};

struct cfdriver p6stats_cd = {
    .cd_devs    = NULL,
    .cd_name    = "p6stats",
    .cd_class   = DV_DULL
};

const struct pci_matchid p6stats_devices[] = {
    { 0x3301, 0x0002 }
};

/* Forward declerations */
int  p6stats_read_event(struct knote *, long);
int  p6stats_write_event(struct knote *, long);
void p6stats_kqdetach(struct knote *);
int p6stats_filt_process(struct knote *, struct kevent *);

const struct filterops p6stats_read_filtops = {
    .f_flags  = FILTEROP_ISFD,
    .f_attach = NULL,               
    .f_detach = p6stats_kqdetach,
    .f_event  = p6stats_read_event,
    .f_modify = NULL,
    .f_process= p6stats_filt_process,
};

const struct filterops p6stats_write_filtops = {
    .f_flags  = FILTEROP_ISFD,
    .f_attach = NULL,
    .f_detach = p6stats_kqdetach,
    .f_event  = p6stats_write_event,
    .f_modify = NULL,
    .f_process = p6stats_filt_process,
};

static int
p6stats_match(struct device *parent, void *match, void *aux)
{
    struct pci_attach_args *pa = aux;
    return (pci_matchbyid(pa, p6stats_devices, nitems(p6stats_devices)));
}

static void
p6stats_attach(struct device *parent, struct device *self, void *aux)
{
    struct p6stats_softc *sc = (struct p6stats_softc *)self;
    struct pci_attach_args *pa = aux;
    pcireg_t memtype;

    sc->sc_pc = pa->pa_pc;
    sc->sc_tag = pa->pa_tag;
    sc->sc_dmat = pa->pa_dmat;

    sc->sc_state = P6_S_READY;

    mtx_init(&sc->sc_mtx, IPL_BIO);

    memtype = pci_mapreg_type(sc->sc_pc, sc->sc_tag, P6_BAR);
    if (pci_mapreg_map(pa, P6_BAR, memtype, 0,
        &sc->sc_memt, &sc->sc_memh, NULL, &sc->sc_mems, 0)) {
        printf(": unable to map register memory\n");
        return;
    }

    if (sc->sc_mems < P6_R_LEN) {
        printf(": register window is too small\n");
        goto unmap;
    }

    /* We create our DMA bus space maps as we did in p6 */
    if (bus_dmamap_create(sc->sc_dmat, P6_I_MAXLEN, 1, P6_I_MAXLEN, 0,
        BUS_DMA_WAITOK | BUS_DMA_ALLOCNOW | BUS_DMA_64BIT,
        &sc->sc_dmap_i) != 0) {
        printf(": unable to create input dma map\n");
        goto unmap;
    }

    if (bus_dmamap_create(sc->sc_dmat, sizeof(struct p6stats_output), 1,
            sizeof(struct p6stats_output), 0, BUS_DMA_WAITOK | BUS_DMA_ALLOCNOW
            | BUS_DMA_64BIT, &sc->sc_dmap_o) != 0) {
        printf(": unable to create output dma map\n");
        goto destroy_i;
    }

    /* We allocate some memory in our output bus for results */
    if (bus_dmamem_alloc(sc->sc_dmat, sizeof(struct p6stats_output),
            sizeof(uint64_t), 0, sc->sc_result_segs, 1,
            &sc->sc_result_nsegs, BUS_DMA_WAITOK | BUS_DMA_ZERO) != 0) {
        printf(": unable to allocate output DMA memory\n");
        goto destroy_o;
    }

    /* We then map this memory so we can reference it from sc->sc_result */
    if (bus_dmamem_map(sc->sc_dmat, sc->sc_result_segs, sc->sc_result_nsegs,
            sizeof(struct p6stats_output), (caddr_t *)&sc->sc_result,
            BUS_DMA_WAITOK | BUS_DMA_COHERENT) != 0) {
        printf(": unable to map output DMA memory\n");
        bus_dmamem_free(sc->sc_dmat, sc->sc_result_segs, sc->sc_result_nsegs);
        goto destroy_o;
    }

    if (pci_intr_map_msix(pa, 0, &sc->sc_ih) != 0) {
        printf(": unable to map interrupt\n");
        goto destroy_o;
    }

    sc->sc_ihc = pci_intr_establish(sc->sc_pc, sc->sc_ih,
        IPL_BIO, p6stats_intr, sc, sc->sc_dev.dv_xname);
    if (sc->sc_ihc == NULL) {
        printf(": unable to establish msix interrupt 0\n");
        goto destroy_o;
    }

    /* initialize klist for kqueue listeners */
    klist_init(&sc->sc_klist, NULL, NULL);

    printf("\n");
    return;

destroy_o:
    bus_dmamap_destroy(sc->sc_dmat, sc->sc_dmap_o);
destroy_i:
    bus_dmamap_destroy(sc->sc_dmat, sc->sc_dmap_i);
unmap:
    bus_space_unmap(sc->sc_memt, sc->sc_memh, sc->sc_mems);
    sc->sc_mems = 0;
}

static struct p6stats_softc *
p6stats_lookup(dev_t dev)
{
    /* the device minor is 1:1 with the driver unit number */
    dev_t unit = minor(dev);
    struct p6stats_softc *sc;

    if (unit >= p6stats_cd.cd_ndevs)
        return (NULL);

    /* this will be NULL if there's no device */
    sc = p6stats_cd.cd_devs[unit];

    return (sc);
}

int
p6statsopen(dev_t dev, int mode, int flags, struct proc *p)
{
    struct p6stats_softc *sc = p6stats_lookup(dev);

    if (sc == NULL) {
        return (ENXIO);
    }
    return (0);
}

int
p6statsclose(dev_t dev, int flags, int mode, struct proc *p)
{
    struct p6stats_softc *sc = p6stats_lookup(dev);

    if (sc == NULL) {
        return (ENXIO);
    }
    return (0);
}

static int
p6stats_intr(void *arg)
{
    struct p6stats_softc *sc = arg;

    mtx_enter(&sc->sc_mtx);
    if (sc->sc_state == P6_S_BUSY) {
        sc->sc_state = P6_S_DONE;
        wakeup(&sc->sc_state);
        /* Notify we are ready to read */
        knote(&sc->sc_klist, 0);
    }
    mtx_leave(&sc->sc_mtx);

    return (1);
}


int
p6statsioctl(dev_t dev, u_long cmd, caddr_t data, int flag, struct proc *p)
{
    return (ENOTTY);
}

int
p6statswrite(dev_t dev, struct uio *uio, int ioflags)
{
    size_t count;

    int error = 0;
    /* Get our software context and check it exists */
    struct p6stats_softc *sc = p6stats_lookup(dev);
    if (sc == NULL) {
        return (ENXIO);
    }

    /* Ensure our result buffer has been allocated */
    if (sc->sc_result == NULL) {
        return (EIO);
    }

    /* Check that the user's buffer is valid */
    if ((uio->uio_resid % sizeof(uint64_t)) != 0) {
        return (EINVAL);
    }

    /* Calculate our count */
    count = uio->uio_resid / sizeof(uint64_t);

    /* Ensure our count is within range */
    if (count > P6_R_ICOUNT_MAX) {
        return (ENOMEM);
    }

    mtx_enter(&sc->sc_mtx);
    /* return immediately if non-blocking and not ready */
    if (ISSET(ioflags, IO_NDELAY)) {
        if (sc->sc_state != P6_S_READY) {
            error = EBUSY;
            goto unlock;
        }
    } else {
        /* Block until we have ready state */
        while (sc->sc_state != P6_S_READY) {
            error = msleep_nsec(&sc->sc_state, &sc->sc_mtx,
                PRIBIO|PCATCH, "p6rdy", INFSLP);
            if (error != 0) {
                goto unlock;
            }
        }
    }

    /* load input from the user's IO */
    error = bus_dmamap_load_uio(sc->sc_dmat, sc->sc_dmap_i, uio,
        BUS_DMA_NOWAIT|BUS_DMA_WRITE);
    if (error != 0) {
        goto unlock;
    }

    /* Load the result memory for DMA to occur */
    error = bus_dmamap_load_raw(sc->sc_dmat, sc->sc_dmap_o,
        sc->sc_result_segs,  sc->sc_result_nsegs,
        sizeof(struct p6stats_output), BUS_DMA_NOWAIT
        | BUS_DMA_READ);
    if (error != 0) {
        bus_dmamap_unload(sc->sc_dmat, sc->sc_dmap_i);
        goto unlock;
    }

    /* Sync to ensure cache isn't caching on our dma maps */
    bus_dmamap_sync(sc->sc_dmat, sc->sc_dmap_i,
        0, sc->sc_dmap_i->dm_segs[0].ds_len,
        BUS_DMASYNC_PREWRITE);

    bus_dmamap_sync(sc->sc_dmat, sc->sc_dmap_o,
        0, sc->sc_dmap_o->dm_segs[0].ds_len,
        BUS_DMASYNC_PREREAD);

    /* Write in our input base address for DMA buffer */
    bus_space_write_8(sc->sc_memt, sc->sc_memh,
        P6_R_IBASE, sc->sc_dmap_i->dm_segs[0].ds_addr);

    /* Write the count of inputs into the device */
    bus_space_write_8(sc->sc_memt, sc->sc_memh,
        P6_R_ICOUNT, count);

    /* Write the address for the output into the buffer */
    bus_space_write_8(sc->sc_memt, sc->sc_memh,
        P6_R_OBASE, sc->sc_dmap_o->dm_segs[0].ds_addr);

    /* Make sure cache isn't caching on our device */
    bus_space_barrier(sc->sc_memt, sc->sc_memh, 0,
        P6_R_LEN, BUS_SPACE_BARRIER_WRITE);

    /* Ring the doorbell to start the operation! */
    bus_space_write_8(sc->sc_memt, sc->sc_memh,
        P6_R_DBELL, 1);

    bus_space_barrier(sc->sc_memt, sc->sc_memh, 0,
        P6_R_LEN, BUS_SPACE_BARRIER_WRITE | BUS_SPACE_BARRIER_READ);

    /* Enter busy state */
    sc->sc_state = P6_S_BUSY;
unlock:
    mtx_leave(&sc->sc_mtx);
    return error;
}

int
p6statsread(dev_t dev, struct uio *uio, int ioflag)
{

    int error = 0;
    /* Get our software context and check it exists */
    struct p6stats_softc *sc = p6stats_lookup(dev);
    if (sc == NULL) {
        return (ENXIO);
    }

    /* Ensure our result buffer has been allocated */
    if (sc->sc_result == NULL) {
        return (EIO);
    }

    /* Check the user has given us enough space for a result */
    if (uio->uio_resid < sizeof(struct p6stats_output)) {
        return (ENOBUFS);
    }

    mtx_enter(&sc->sc_mtx);

    /* Return immediately if not done and nonblocking */
    if (ISSET(ioflag, IO_NDELAY)) {
        if (sc->sc_state != P6_S_DONE) {
            error = EAGAIN;
            goto unlock;
        }
    } else {
        /* Wait for our result */
        while (sc->sc_state != P6_S_DONE) {
            error = msleep_nsec(&sc->sc_state, &sc->sc_mtx,
                PRIBIO|PCATCH, "p6wait", INFSLP);
            if (error!= 0)
                goto unlock;
        }
    }

    /* Sync to ensure cache isn't caching on our dma maps */
    bus_dmamap_sync(sc->sc_dmat, sc->sc_dmap_o,
        0, sc->sc_dmap_o->dm_segs[0].ds_len,
        BUS_DMASYNC_POSTREAD);

    bus_dmamap_sync(sc->sc_dmat, sc->sc_dmap_i,
        0, sc->sc_dmap_i->dm_segs[0].ds_len,
        BUS_DMASYNC_POSTWRITE);

    /* Give userland our result */
    error = uiomove(sc->sc_result, sizeof(struct p6stats_output), uio);
    if (error != 0) {
        printf("%s: Error in transfering data to userland\r\n", sc->sc_dev.dv_xname);
        goto reset;
    }

    /* Unload our maps -- DMA has finished */
    bus_dmamap_unload(sc->sc_dmat, sc->sc_dmap_o);
    bus_dmamap_unload(sc->sc_dmat, sc->sc_dmap_i);

    /* notify kqueue listeners that writers may proceed */
    knote(&sc->sc_klist, 0);
reset:
    /* Go back into ready state and let something else have a go */
    sc->sc_state = P6_S_READY;
    wakeup(&sc->sc_state);
unlock:
    mtx_leave(&sc->sc_mtx);
    return error;
}

int
p6stats_read_event(struct knote *kn, long hint)
{
    struct p6stats_softc *sc = kn->kn_hook;
    int ready;

    /* Syscalls enter through process, knote() must always be called under mutex */
    MUTEX_ASSERT_LOCKED(&sc->sc_mtx);
    
    ready = (sc->sc_state == P6_S_DONE);
    if (ready)
        kn->kn_data = sizeof(struct p6stats_output);
    else
        kn->kn_data = 0;

    return ready;
}

int
p6stats_write_event(struct knote *kn, long hint)
{
    struct p6stats_softc *sc = kn->kn_hook;
    int ready;
    
    /* Syscalls enter through process, knote() must always be called under mutex */
    MUTEX_ASSERT_LOCKED(&sc->sc_mtx);

    ready = (sc->sc_state == P6_S_READY);
    kn->kn_data = ready ? 1 : 0;

    return ready;
}

int
p6statskqfilter(dev_t dev, struct knote *kn)
{

    struct p6stats_softc *sc = p6stats_lookup(dev);
    if (sc == NULL)
        return (ENXIO);

    switch (kn->kn_filter) {
    case EVFILT_READ:
        /* bind our read op */
        kn->kn_fop = &p6stats_read_filtops;
        break;
    case EVFILT_WRITE:
        /* bind our write op */
        kn->kn_fop = &p6stats_write_filtops;
        break;
    default:
        return (EINVAL);
    }

    /* attach now: bind knote to softc and add to our list */
    kn->kn_hook = sc;
    mtx_enter(&sc->sc_mtx);
    klist_insert(&sc->sc_klist, kn);
    mtx_leave(&sc->sc_mtx);

    return 0;
}

void
p6stats_kqdetach(struct knote *kn)
{
    /* ensure we remove the klist before leaving */
    struct p6stats_softc *sc = kn->kn_hook;
    mtx_enter(&sc->sc_mtx);
    klist_remove(&sc->sc_klist, kn);
    mtx_leave(&sc->sc_mtx);
}


int 
p6stats_filt_process(struct knote *kn, struct kevent *kev)
{
    struct p6stats_softc *sc = kn->kn_hook;
    int active;
    /* When entered from a syscall we can take the lock */
    mtx_enter(&sc->sc_mtx);
    active = knote_process(kn, kev);
    mtx_leave(&sc->sc_mtx);

    return (active);
}
