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

#include <sys/syscall.h>
#include <sys/socket.h>
#include <sys/mount.h>
#include <sys/syscallargs.h>

static int    p4d_match(struct device *, void *, void *);
static void    p4d_attach(struct device *, struct device *, void *);

struct p4d_softc {
    struct device         sc_dev;
    struct rwlock         sc_lock;
    bus_space_tag_t         sc_bar_tag;
    bus_space_handle_t     sc_bar_hdl;
    struct p4d_bar        *sc_bar;
};

const struct cfattach p4d_ca = {
    .ca_devsize     = sizeof(struct p4d_softc),
    .ca_match     = p4d_match,
    .ca_attach     = p4d_attach
};

struct cfdriver p4d_cd = {
    .cd_devs     = NULL,
    .cd_name    = "p4d",
    .cd_class    = DV_DULL
};

static int
p4d_match(struct device *parent, void *match, void *aux)
{
    struct pci_attach_args *pa = aux;
    if (PCI_VENDOR(pa->pa_id) == 0x3301 &&
        PCI_PRODUCT(pa->pa_id) == 0x0001)
        return (1);
    return (0);
}

struct p4d_bar {
    uint64_t    a;
    uint64_t    b;
    uint64_t    sum;
};

static void
p4d_attach(struct device *parent, struct device *self, void *aux)
{
    struct p4d_softc *sc = (struct p4d_softc *)self;
    struct pci_attach_args *pa = aux;
    bus_size_t bar_size;
    pcireg_t regtype;
    int rc;

    rw_init(&sc->sc_lock, "p4d");

    regtype = pci_mapreg_type(pa->pa_pc, pa->pa_tag, 0x10);
    rc = pci_mapreg_map(pa, 0x10, regtype, BUS_SPACE_MAP_LINEAR,
        &sc->sc_bar_tag, &sc->sc_bar_hdl, NULL, &bar_size, 0);
    if (rc != 0) {
        printf(": failed to map BAR: %d\n", rc);
        return;
    }

    if (bar_size < sizeof(struct p4d_bar)) {
        printf(": BAR is too small! (%zx but expected at"
            " least %zx)\n", bar_size, sizeof(struct p4d_bar));
        return;
    }

    sc->sc_bar = bus_space_vaddr(sc->sc_bar_tag, sc->sc_bar_hdl);

    sc->sc_bar->sum = 0;
    bus_space_barrier(sc->sc_bar_tag, sc->sc_bar_hdl, 0,
        sizeof (struct p4d_bar), BUS_SPACE_BARRIER_WRITE);
    printf(": ok\n");
}

int
sys_add2(struct proc *p, void *v, register_t *retval)
{
    struct p4d_softc *sc;
    struct sys_add2_args *uap = v;
    uint64_t a = SCARG(uap, a);
    uint64_t b = SCARG(uap, b);
    uint64_t sum;
    uint64_t *result = (uint64_t *)SCARG(uap, result);
    int rc;

    if (p4d_cd.cd_ndevs < 1)
        return (ENODEV);
    sc = p4d_cd.cd_devs[0];
    if (sc == NULL)
        return (ENODEV);

    rw_enter_write(&sc->sc_lock);

    sc->sc_bar->sum = 0;
    bus_space_barrier(sc->sc_bar_tag, sc->sc_bar_hdl, 0,
        sizeof (struct p4d_bar), BUS_SPACE_BARRIER_WRITE);
    
    sc->sc_bar->a = a;
    sc->sc_bar->b = b;
    bus_space_barrier(sc->sc_bar_tag, sc->sc_bar_hdl, 0,
        sizeof (struct p4d_bar),
        BUS_SPACE_BARRIER_WRITE | BUS_SPACE_BARRIER_READ);

    sum = sc->sc_bar->sum;
    rc = copyout(&sum, result, sizeof (sum));

    rw_exit_write(&sc->sc_lock);

    return (rc);
}