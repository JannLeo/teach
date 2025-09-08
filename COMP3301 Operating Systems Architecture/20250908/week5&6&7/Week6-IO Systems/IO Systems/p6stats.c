#include <sys/param.h>
#include <sys/systm.h>
#include <sys/errno.h>
#include <sys/ioctl.h>
#include <sys/fcntl.h>
#include <sys/device.h>
#include <sys/vnode.h>
#include <sys/atomic.h>

#include <machine/bus.h>

#include <dev/pci/pcireg.h>
#include <dev/pci/pcivar.h>
#include <dev/pci/pcidevs.h>

#include <dev/pci/p6statsvar.h>

#define P6_BAR            PCI_MAPREG_START /* BAR 0 */

#define P6_R_IBASE        0x00
#define P6_R_ICOUNT        0x08
#define  P6_R_ICOUNT_MAX        512 /* how long is a bit of string? */
#define P6_R_OBASE        0x10
#define P6_R_DBELL        0x18
#define P6_R_LEN        0x20

#define P6_I_MAXLEN (sizeof(uint64_t) * P6_R_ICOUNT_MAX)

#define P6_S_READY        0
#define P6_S_BUSY        1
#define P6_S_DONE        2

struct p6stats_softc {
    struct device         sc_dev;

    pci_chipset_tag_t     sc_pc;
    pci_intr_handle_t     sc_ih;
    void            *sc_ihc;
    pcitag_t         sc_tag;

    bus_dma_tag_t         sc_dmat;
    bus_space_tag_t         sc_memt;
    bus_space_handle_t     sc_memh;
    bus_size_t         sc_mems;

    bus_dmamap_t         sc_dmap_i;
    bus_dmamap_t         sc_dmap_o;

    struct mutex         sc_mtx;
    unsigned int         sc_state;
};

static int    p6stats_match(struct device *, void *, void *);
static void    p6stats_attach(struct device *, struct device *, void *);

static int    p6stats_intr(void *);

const struct cfattach p6stats_ca = {
    .ca_devsize    = sizeof(struct p6stats_softc),
    .ca_match    = p6stats_match,
    .ca_attach    = p6stats_attach
};

struct cfdriver p6stats_cd = {
    .cd_devs    = NULL,
    .cd_name    = "p6stats",
    .cd_class    = DV_DULL
};

const struct pci_matchid p6stats_devices[] = {
    { 0x3301, 0x0002 }
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

    if (bus_dmamap_create(sc->sc_dmat, P6_I_MAXLEN, 1, P6_I_MAXLEN, 0,
        BUS_DMA_WAITOK | BUS_DMA_ALLOCNOW | BUS_DMA_64BIT,
        &sc->sc_dmap_i) != 0) {
        printf(": unable to create input dma map\n");
        goto unmap;
    }

    if (bus_dmamap_create(sc->sc_dmat, sizeof(struct p6stats_output), 1,
        sizeof(struct p6stats_output), 0,
        BUS_DMA_WAITOK | BUS_DMA_ALLOCNOW | BUS_DMA_64BIT,
        &sc->sc_dmap_o) != 0) {
        printf(": unable to create output dma map\n");
        goto destroy_i;
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

    if (sc == NULL)
        return (ENXIO);

    return (0);
}

int
p6statsclose(dev_t dev, int flag, int mode, struct proc *p)
{
    /* replace with your code */
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
    }
    mtx_leave(&sc->sc_mtx);

    return (1);
}

static int
p6stats_calc(struct proc *p, struct p6stats_softc *sc, struct p6stats_calc *pc)
{
    struct uio uio_i, uio_o;
    struct iovec iov_i[1], iov_o[1];
    int error;

    if (pc->pc_ninputs > P6_R_ICOUNT_MAX)
        return (ENOMEM);

    /* map inputs to a uio */
    iov_i[0].iov_base = pc->pc_inputs;
    iov_i[0].iov_len = pc->pc_ninputs * sizeof(*pc->pc_inputs);

    uio_i.uio_iov = iov_i;
    uio_i.uio_iovcnt = nitems(iov_i);
    uio_i.uio_offset = 0;
    uio_i.uio_resid = iov_i[0].iov_len;
    uio_i.uio_rw = UIO_WRITE;
    uio_i.uio_segflg = UIO_USERSPACE;
    uio_i.uio_procp = p;

    /* map output to another uio */
    iov_o[0].iov_base = pc->pc_output;
    iov_o[0].iov_len = sizeof(*pc->pc_output);

    uio_o.uio_iov = iov_o;
    uio_o.uio_iovcnt = nitems(iov_o);
    uio_o.uio_offset = 0;
    uio_o.uio_resid = iov_o[0].iov_len;
    uio_o.uio_rw = UIO_READ;
    uio_o.uio_segflg = UIO_USERSPACE;
    uio_o.uio_procp = p;

    mtx_enter(&sc->sc_mtx);
    while (sc->sc_state != P6_S_READY) {
        error = msleep_nsec(&sc->sc_state, &sc->sc_mtx,
            PRIBIO|PCATCH, "p6rdy", INFSLP);
        if (error != 0)
            goto unlock;
    }

    error = bus_dmamap_load_uio(sc->sc_dmat, sc->sc_dmap_i, &uio_i,
        BUS_DMA_NOWAIT|BUS_DMA_WRITE);
    if (error != 0)
        goto unlock;

    error = bus_dmamap_load_uio(sc->sc_dmat, sc->sc_dmap_o, &uio_o,
        BUS_DMA_NOWAIT|BUS_DMA_READ);
    if (error != 0)
        goto unload_i;

    bus_dmamap_sync(sc->sc_dmat, sc->sc_dmap_i,
        0, sc->sc_dmap_i->dm_segs[0].ds_len,
        BUS_DMASYNC_PREWRITE);

    bus_dmamap_sync(sc->sc_dmat, sc->sc_dmap_o,
        0, sc->sc_dmap_o->dm_segs[0].ds_len,
        BUS_DMASYNC_PREREAD);

    bus_space_write_8(sc->sc_memt, sc->sc_memh,
        P6_R_IBASE, sc->sc_dmap_i->dm_segs[0].ds_addr);
    bus_space_write_8(sc->sc_memt, sc->sc_memh,
        P6_R_ICOUNT, pc->pc_ninputs);
    bus_space_write_8(sc->sc_memt, sc->sc_memh,
        P6_R_OBASE, sc->sc_dmap_o->dm_segs[0].ds_addr);
    bus_space_barrier(sc->sc_memt, sc->sc_memh, 0,
        P6_R_LEN, BUS_SPACE_BARRIER_WRITE);
    bus_space_write_8(sc->sc_memt, sc->sc_memh,
        P6_R_DBELL, 1);

    /*
     * p6stats_intr can't change sc_state until we give up the
     * mtx in msleep.
     */
    sc->sc_state = P6_S_BUSY;
    do {
        msleep_nsec(&sc->sc_state, &sc->sc_mtx,
            PRIBIO, "p6wait", INFSLP);
        /*
                 * XXX what can we do if there's no interrupt? the
                 * hardware owns the memory, and until we know it
                 * won't touch it then it's not safe to use.
         */
    } while (sc->sc_state != P6_S_DONE);

    bus_dmamap_sync(sc->sc_dmat, sc->sc_dmap_o,
        0, sc->sc_dmap_o->dm_segs[0].ds_len,
        BUS_DMASYNC_POSTREAD);

    bus_dmamap_sync(sc->sc_dmat, sc->sc_dmap_i,
        0, sc->sc_dmap_i->dm_segs[0].ds_len,
        BUS_DMASYNC_POSTWRITE);

    bus_dmamap_unload(sc->sc_dmat, sc->sc_dmap_o);
    bus_dmamap_unload(sc->sc_dmat, sc->sc_dmap_i);

    sc->sc_state = P6_S_READY;
    wakeup(&sc->sc_mtx); /* let something else have a go */

unload_i:
    bus_dmamap_unload(sc->sc_dmat, sc->sc_dmap_i);
unlock:
    mtx_leave(&sc->sc_mtx);
    return (error);
}

int
p6statsioctl(dev_t dev, u_long cmd, caddr_t data, int flag, struct proc *p)
{
    struct p6stats_softc *sc = p6stats_lookup(dev);
    int error = 0;

    switch (cmd) {
    case P6STATS_IOC_CALC:
        error = p6stats_calc(p, sc, (struct p6stats_calc *)data);
        break;

    default:
        error = ENOTTY;
        break;
    }

    return (error);
}