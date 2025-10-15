/*
 * Copyright (c) 2025 The University of Queensland
 *
 * Permission to use, copy, modify, and distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 *
 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 * ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 * ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 * OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 */

#include <sys/param.h>
#include <sys/systm.h>
#include <sys/namei.h>
#include <sys/proc.h>
#include <sys/errno.h>
#include <sys/limits.h>
#include <sys/buf.h>
#include <sys/malloc.h>
#include <sys/ioctl.h>
#include <sys/disklabel.h>
#include <sys/device.h>
#include <sys/disk.h>
#include <sys/stat.h>
#include <sys/vnode.h>
#include <sys/lock.h>
#include <sys/fcntl.h>
#include <sys/uio.h>
#include <sys/conf.h>
#include <sys/dkio.h>
#include <sys/specdev.h>
#include <sys/tree.h>

#include <dev/fvdvar.h>

struct fvd_softc {
	struct device		 sc_dev;
	RBT_ENTRY(fvd_softc)	 sc_entry;
	struct refcnt		 sc_refs;

	struct disk		 sc_dk;

	char			*sc_fname;		/* fvd path */
	size_t			 sc_fnamelen;		/* path length */
	char			 sc_bname[FVD_MAX_BNM];	/* branch name */
	struct vnode		*sc_fvdvp;		/* fvd vnode */
	struct vnode		*sc_refvp;		/* ref vnode */
	struct ucred		*sc_ucred;		/* vnode creds */
	int			 sc_rw;			/* read/write mode */

	/* fill these out in fvd_attach */
	uint32_t		 sc_cylinders;	/* cylinder count */
	uint32_t		 sc_heads;	/* head count */
	uint32_t		 sc_spt;	/* sectors per track */
};

RBT_HEAD(fvd_softcs, fvd_softc);

static inline int
fvd_cmp(const struct fvd_softc *a, const struct fvd_softc *b)
{
	const struct device *da = &a->sc_dev;
	const struct device *db = &b->sc_dev;

	if (da->dv_unit > db->dv_unit)
		return (1);
	if (da->dv_unit < db->dv_unit)
		return (-1);
	return (0);
}

RBT_PROTOTYPE(fvd_softcs, fvd_softc, sc_entry, fvd_cmp);

struct fvd_driver {
	struct fvd_softcs		fd_scs;
	struct rwlock			fd_lock;
};

static struct fvd_driver fd = {
	.fd_scs		= RBT_INITIALIZER(),
	.fd_lock	= RWLOCK_INITIALIZER("fvddrv")
};

static int	fvd_getdisklabel(dev_t, struct fvd_softc *,
		    struct disklabel *, int);

void
fvdattach(int num)
{
	/* fd is already set up */
}

/*
 * Function used to checksum a sector. Declared as weak to make the base code
 * compile and link correctly when there's no code actually calling this
 * function yet.
 */
__attribute__((weak)) uint32_t	/* CSTYLED */
fvd_csum_sect(const void *buf)
{
	const uint8_t *data = buf;
	uint32_t sum1 = 0xFFFF, sum2 = 0xFFFF;

	for (size_t i = 0; i < FVD_SECTOR_SIZE; i++) {
		sum1 = (sum1 + data[i]) % 0xFFFF;
		sum2 = (sum2 + sum1) % 0xFFFF;
	}

	return (sum2 << 16) | sum1;
}

static struct fvd_softc *
fvd_find(dev_t dev)
{
	struct device key = {
		.dv_unit = DISKUNIT(dev)
	};

	return (RBT_FIND(fvd_softcs, &fd.fd_scs,
	    (const struct fvd_softc *)&key));
}

static struct fvd_softc *
fvd_create(dev_t dev)
{
	int unit = DISKUNIT(dev);
	struct fvd_softc *sc;
	struct device *dv;

	sc = malloc(sizeof(*sc), M_DEVBUF, M_WAITOK|M_CANFAIL|M_ZERO);
	if (sc == NULL)
		return (NULL);

	refcnt_init(&sc->sc_refs);

	dv = &sc->sc_dev;
	dv->dv_class = DV_DISK;
	dv->dv_unit = unit;
	if (snprintf(dv->dv_xname, sizeof(dv->dv_xname),
	    "fvd%d", dv->dv_unit) >= sizeof(dv->dv_xname))
		panic("%s dv_xname printf", __func__);
	dv->dv_ref = 1;

	sc->sc_dk.dk_name = dv->dv_xname;

	return (sc); /* give ref to the caller */
}

static int
fvd_insert(struct fvd_softc *sc)
{
	if (RBT_INSERT(fvd_softcs, &fd.fd_scs, sc) != NULL)
		return (EBUSY);

	refcnt_take(&sc->sc_refs); /* take one for the tree */
	return (0);
}

static void
fvd_remove(struct fvd_softc *sc)
{
	RBT_REMOVE(fvd_softcs, &fd.fd_scs, sc);
	refcnt_rele(&sc->sc_refs); /* caller must be holding a ref too */
}

static struct fvd_softc *
fvd_enter(dev_t dev)
{
	struct fvd_softc *sc;

	rw_enter_read(&fd.fd_lock);
	sc = fvd_find(dev);
	if (sc != NULL)
		refcnt_take(&sc->sc_refs);
	rw_exit_read(&fd.fd_lock);

	return (sc);
}

static void
fvd_leave(struct fvd_softc *sc)
{
	if (refcnt_rele(&sc->sc_refs)) {
		KASSERT(sc->sc_dev.dv_ref == 1);

		vn_close(sc->sc_fvdvp, sc->sc_rw, sc->sc_ucred, curproc);
		vn_close(sc->sc_refvp, sc->sc_rw, sc->sc_ucred, curproc);
		crfree(sc->sc_ucred);

		free(sc->sc_fname, M_DEVBUF, sc->sc_fnamelen);
		free(sc, M_DEVBUF, sizeof(*sc));
	}
}

static int
fvd_disk_open(struct fvd_softc *sc, int part, int mode)
{
	int error;

	error = disk_lock(&sc->sc_dk);
	if (error != 0)
		return (0);

	error = disk_openpart(&sc->sc_dk, part, mode, 1);
	disk_unlock(&sc->sc_dk);

	return (error);
}

int
fvdopen(dev_t dev, int flags, int fmt, struct proc *p)
{
	dev_t part = DISKPART(dev);
	struct fvd_softc *sc;
	int raw = part == RAW_PART && fmt == S_IFCHR;
	int error;

	sc = fvd_enter(dev);
	if (sc == NULL) {
		/* allow opens of /dev/rfvdXc for attach ioctls */
		if (raw)
			return (0);

		return (ENXIO);
	}

	if (ISSET(flags, FWRITE) && !ISSET(sc->sc_rw, FWRITE) && !raw) {
		error = EACCES;
		goto leave;
	}

	if (sc->sc_dk.dk_openmask == 0) {
		error = fvd_getdisklabel(dev, sc, sc->sc_dk.dk_label, 0);
		if (error == EIO || error == ENXIO)
			goto leave;
	}

	error = fvd_disk_open(sc, part, fmt);

leave:
	fvd_leave(sc);

	return (error);
}

int
fvdclose(dev_t dev, int flags, int fmt, struct proc *p)
{
	dev_t part = DISKPART(dev);
	struct fvd_softc *sc;

	sc = fvd_enter(dev);
	if (sc == NULL) {
		return (0);
	}

	disk_lock_nointr(&sc->sc_dk);
	disk_closepart(&sc->sc_dk, part, fmt);
	disk_unlock(&sc->sc_dk);
	fvd_leave(sc);

	return (0);
}

static int
fvd_read_sect(struct fvd_softc *sc, uint32_t sec, void *buf)
{
	/* <YOUR CODE HERE> */
	return (ENOSYS);
}

static int
fvd_write_sect(struct fvd_softc *sc, uint32_t sec, const void *buf)
{
	/* <YOUR CODE HERE> */
	return (ENOSYS);
}

static size_t
fvd_read(struct fvd_softc *sc, uint64_t offset, void *buf, size_t toread,
    int *err)
{
	size_t sectoff, partlen;
	uint32_t sec, nsecs, i;
	uint8_t sector[FVD_SECTOR_SIZE];
	int error;

	KASSERT(sc != NULL && (!toread || (toread && buf)));

	error = 0;
	if (!toread)
		goto out;

	/* handle partial sector if not starting at sector boundary */
	sectoff = offset % FVD_SECTOR_SIZE;
	if (sectoff) {
		partlen = FVD_SECTOR_SIZE - sectoff;
		error = fvd_read_sect(sc, offset / FVD_SECTOR_SIZE, sector);
		if (error)
			goto out;
		memcpy(buf, &sector[sectoff], partlen);
		buf += partlen;
		offset += partlen;
		toread -= partlen;
	}

	sec = offset / FVD_SECTOR_SIZE;
	nsecs = toread / FVD_SECTOR_SIZE;

	/* read all complete sectors */
	for (i = 0; i < nsecs; i++) {
		if ((error = fvd_read_sect(sc, sec, buf)))
			goto out;
		sec++;
		buf += FVD_SECTOR_SIZE;
		toread -= FVD_SECTOR_SIZE;
	}

	/* see if we have a partial sector at the end */
	if (toread) {
		if ((error = fvd_read_sect(sc, sec, sector)))
			goto out;
		memcpy(buf, sector, toread);
		toread = 0;
	}

out:
	*err = error;
	return (toread);
}

static size_t
fvd_write(struct fvd_softc *sc, uint64_t offset, const void *buf,
    size_t towrite, int *err)
{
	size_t sectoff, partlen;
	uint32_t sec, nsecs, i;
	uint8_t sector[FVD_SECTOR_SIZE];
	int error;

	KASSERT(sc != NULL && (!towrite || (towrite && buf)));

	error = 0;
	if (!towrite)
		goto out;

	/* handle partial sector if not starting at sector boundary */
	sectoff = offset % FVD_SECTOR_SIZE;
	if (sectoff) {
		partlen = FVD_SECTOR_SIZE - sectoff;
		error = fvd_read_sect(sc, offset / FVD_SECTOR_SIZE, sector);
		if (error)
			goto out;
		memcpy(&sector[sectoff], buf, partlen);
		error = fvd_write_sect(sc, offset / FVD_SECTOR_SIZE, sector);
		if (error)
			goto out;
		buf += partlen;
		offset += partlen;
		towrite -= partlen;
	}

	sec = offset / FVD_SECTOR_SIZE;
	nsecs = towrite / FVD_SECTOR_SIZE;

	/* write all complete sectors */
	for (i = 0; i < nsecs; i++) {
		if ((error = fvd_write_sect(sc, sec, buf)))
			goto out;
		sec++;
		buf += FVD_SECTOR_SIZE;
		towrite -= FVD_SECTOR_SIZE;
	}

	/* see if we have a partial sector at the end */
	if (towrite) {
		if ((error = fvd_read_sect(sc, sec, sector)))
			goto out;
		memcpy(sector, buf, towrite);
		if ((error = fvd_write_sect(sc, sec, sector)))
			goto out;
		towrite = 0;
	}

out:
	*err = error;
	return (towrite);
}

void
fvdstrategy(struct buf *bp)
{
	struct fvd_softc *sc;
	struct partition *p;
	size_t resid;
	int s;

	sc = fvd_enter(bp->b_dev);
	if (sc == NULL) {
		bp->b_error = ENXIO;
		goto bad;
	}

	p = &sc->sc_dk.dk_label->d_partitions[DISKPART(bp->b_dev)];
	off_t off = DL_GETPOFFSET(p) * sc->sc_dk.dk_label->d_secsize +
	    (u_int64_t)bp->b_blkno * DEV_BSIZE;

	if (bounds_check_with_label(bp, sc->sc_dk.dk_label) == -1) {
		bp->b_resid = bp->b_bcount;
		goto leave;
	}

	if (bp->b_flags & B_READ)
		resid = fvd_read(sc, (uint64_t)off, (void *)bp->b_data,
		    bp->b_bcount, &bp->b_error);
	else
		resid = fvd_write(sc, (uint64_t)off, (const void *)bp->b_data,
		    bp->b_bcount, &bp->b_error);

	bp->b_resid = resid;
	if (bp->b_error)
		bp->b_flags |= B_ERROR;

leave:
	fvd_leave(sc);
	goto done;
bad:
	bp->b_flags |= B_ERROR;
	bp->b_resid = bp->b_bcount;
done:
	s = splbio();
	biodone(bp);
	splx(s);
}

int
fvdread(dev_t dev, struct uio *uio, int flags)
{
	return (physio(fvdstrategy, dev, B_READ, minphys, uio));
}

int
fvdwrite(dev_t dev, struct uio *uio, int flags)
{
	return (physio(fvdstrategy, dev, B_WRITE, minphys, uio));
}

static int
fvd_vnopen(const char *fname, int rw, struct vnode **vp, struct proc *p)
{
	struct nameidata nd;
	int error;

	NDINIT(&nd, 0, 0, UIO_SYSSPACE, fname, p);
	nd.ni_unveil = UNVEIL_READ;
	if (rw & FWRITE) {
		nd.ni_unveil |= UNVEIL_WRITE;
	}
	error = vn_open(&nd, rw, 0);
	if (error != 0)
		return (error);

	*vp = nd.ni_vp;
	VOP_UNLOCK(*vp);
	if ((*vp)->v_type != VREG) {
		error = EOPNOTSUPP;
		vn_close(*vp, rw, p->p_ucred, p);
	}
	return (error);
}

static int
fvd_attach(dev_t dev, int flag, const struct fvd_attach *fa, struct proc *p)
{
	struct fvd_softc *sc;
	int part = DISKPART(dev);
	struct vnode *fvdvp;
	struct vnode *refvp;
	char fname[PATH_MAX + 4];
	char bname[FVD_MAX_BNM];
	size_t fnamelen;
	int rw;
	int error;

	/*
	 * we can't be here without this being true, but it's
	 * nice to be sure.
	 */
	if (part != RAW_PART || !vfinddev(dev, VCHR, &fvdvp))
		return (ENOTTY);
	if (!ISSET(flag, FWRITE))
		return (EBADF);

	error = rw_enter(&fd.fd_lock, RW_WRITE|RW_INTR);
	if (error != 0)
		return (error);

	sc = fvd_find(dev);
	rw_exit(&fd.fd_lock);
	if (sc != NULL)
		return (EBUSY);

	/* get path to .fvd */
	error = copyinstr(fa->fa_path, fname, sizeof(fname), &fnamelen);
	if (error != 0)
		return (error);

	/* make sure has enough space for ".ref" */
	if (fnamelen > sizeof(fname) - 4)
		return (ENAMETOOLONG);

	error = copyinstr(fa->fa_branch, bname, sizeof(bname), NULL);
	if (error != 0)
		return (error);

	/* figure out file open mode */
	rw = FREAD;
	if (!fa->fa_readonly) {
		rw |= FWRITE;
	}

	/* open disk container file */
	error = fvd_vnopen(fname, rw, &fvdvp, p);
	if (error != 0)
		return (error);

	/* open refcount metadata file */
	strlcat(fname, ".ref", sizeof(fname));
	error = fvd_vnopen(fname, rw, &refvp, p);
	fname[fnamelen - 1] = '\0';
	if (error != 0)
		goto closefvd;

	sc = fvd_create(dev);
	if (sc == NULL) {
		error = ENOMEM;
		goto closeref;
	}

	sc->sc_fname = malloc(fnamelen, M_DEVBUF, M_WAITOK|M_CANFAIL);
	if (sc->sc_fname == NULL) {
		error = ENOMEM;
		goto destroy;
	}

	memcpy(sc->sc_fname, fname, fnamelen);
	sc->sc_fnamelen = fnamelen;
	strlcpy(sc->sc_bname, bname, sizeof(sc->sc_bname));
	sc->sc_fvdvp = fvdvp;
	sc->sc_refvp = refvp;
	sc->sc_ucred = crhold(p->p_ucred);
	sc->sc_rw = rw;

	/*
	 * <YOUR CODE HERE>
	 *
	 * Remember to set sc_cylinders, sc_heads and sc_spt in the softc
	 * struct.
	 */

	error = rw_enter(&fd.fd_lock, RW_WRITE|RW_INTR);
	if (error != 0)
		goto freeup;

	error = fvd_insert(sc);
	if (error != 0)
		goto rollback;

	disk_attach(&sc->sc_dev, &sc->sc_dk);

	fvd_leave(sc);
	rw_exit(&fd.fd_lock);

	return (error);

rollback:
	rw_exit(&fd.fd_lock);
freeup:
	crfree(sc->sc_ucred);
	free(sc->sc_fname, M_DEVBUF, sc->sc_fnamelen);
destroy:
	free(sc, M_DEVBUF, sizeof(*sc));
closeref:
	vn_close(refvp, rw, p->p_ucred, p);
closefvd:
	vn_close(fvdvp, rw, p->p_ucred, p);
	return (error);
}

static int
fvd_detach(struct fvd_softc *sc, dev_t dev, int flag, unsigned int force)
{
	struct vnode *vp;
	int part = DISKPART(dev);
	int error;

	if (part != RAW_PART || !vfinddev(dev, VCHR, &vp))
		return (ENOTTY);
	if (!ISSET(flag, FWRITE))
		return (EBADF);

	error = rw_enter(&fd.fd_lock, RW_WRITE|RW_INTR);
	if (error != 0)
		return (error);

	if (!force) {
		struct disk *dk = &sc->sc_dk;
		int pmask = (1 << part);

		error = disk_lock(dk);
		if (error != 0)
			goto leave;

		if (ISSET(dk->dk_copenmask, ~pmask) || dk->dk_bopenmask)
			error = EBUSY;

		disk_unlock(&sc->sc_dk);

		if (error != 0)
			goto leave;
	}

	fvd_remove(sc);
	rw_exit(&fd.fd_lock);

	disk_gone(fvdopen, sc->sc_dev.dv_unit);
	disk_detach(&sc->sc_dk);

	return (0);

leave:
	rw_exit(&fd.fd_lock);
	return (error);
}

int
fvdioctl(dev_t dev, u_long cmd, caddr_t data, int flag, struct proc *p)
{
	struct fvd_softc *sc;
	struct disklabel *lp;
	int error = 0;

	if (cmd == FVDIOC_ATTACH)
		return (fvd_attach(dev, flag, (struct fvd_attach *)data, p));

	/* everything else needs an attached disk */
	sc = fvd_enter(dev);
	if (sc == NULL)
		return (ENXIO);

	switch (cmd) {
	case FVDIOC_DETACH:
		error = fvd_detach(sc, dev, flag, *(unsigned int *)data);
		break;

	case DIOCRLDINFO:
		lp = malloc(sizeof(*lp), M_TEMP, M_WAITOK);
		fvd_getdisklabel(dev, sc, lp, 0);
		*(sc->sc_dk.dk_label) = *lp;
		free(lp, M_TEMP, sizeof(*lp));
		break;

	case DIOCGPDINFO:
		fvd_getdisklabel(dev, sc, (struct disklabel *)data, 1);
		break;

	case DIOCGDINFO:
		*(struct disklabel *)data = *(sc->sc_dk.dk_label);
		break;

	case DIOCGPART:
		((struct partinfo *)data)->disklab = sc->sc_dk.dk_label;
		((struct partinfo *)data)->part =
		    &sc->sc_dk.dk_label->d_partitions[DISKPART(dev)];
		break;

	case DIOCWDINFO:
	case DIOCSDINFO:
		if (!ISSET(flag, FWRITE)) {
			error = EBADF;
			break;
		}

		error = disk_lock(&sc->sc_dk);
		if (error != 0)
			break;

		error = setdisklabel(sc->sc_dk.dk_label,
		    (struct disklabel *)data, sc->sc_dk.dk_openmask);
		if (error == 0) {
			if (cmd == DIOCWDINFO)
				error = writedisklabel(DISKLABELDEV(dev),
				    fvdstrategy, sc->sc_dk.dk_label);
		}

		disk_unlock(&sc->sc_dk);
		break;

	default:
		error = ENOTTY;
		break;
	}

	fvd_leave(sc);

	return (error);
}

daddr_t
fvdsize(dev_t dev)
{
	/* we don't support swapping to fvd. */
	return (-1);
}

int
fvddump(dev_t dev, daddr_t blkno, caddr_t va, size_t size)
{
	/* we don't support dumping to fvd. */
	return (ENXIO);
}

static int
fvd_getdisklabel(dev_t dev, struct fvd_softc *sc, struct disklabel *lp,
    int spoofonly)
{
	memset(lp, 0, sizeof(*lp));

	/* disk geometry (i hate this stuff) --dlg, 2023 */

	/*
	 * For this assignment, you can just completely ignore all of this
	 * stuff, it's been taken care of for you here :). If you do want to
	 * fry your brain a bit though, read on...
	 *
	 * A disk can have many heads (a head is a surface of a disk platter),
	 * and each head contains a number of tracks, with each track
	 * containing a number of sectors. A cylinder is a conceptual vertical
	 * column of tracks, consisting of one track from each platter surface
	 * at the same radius.
	 *
	 * In CHS addressing, C means cylinder count (number of tracks per
	 * head), H means head count (number of platter surfaces in the disk)
	 * and S means the number of sectors per track.
	 *
	 * So:
	 * 	TPH (tracks per head) = C in CHS
	 * 	HPD (heads per disk) = H in CHS
	 * 	SPT (sectors per track) = S in CHS
	 *
	 * 	d_nsectors = SPT
	 * 	d_ntracks = HPD
	 * 	d_ncylinders = TPH
	 * 	d_secpercyl = HPD * SPT
	 * 	d_secperunit = SPT * TPH * HPD
	 *
	 * All of this setup is done for you already, you just need to set
	 * .sc_spt to S in CHS, .sc_cylinders to C in CHS and .sc_heads to
	 * H in CHS in the softc and it'll work.
	 *
	 * Lastly, I also hate this stuff. --Yufeng, 2024
	 *
	 * ... and I got some of it wrong last year... now fixed. I really
	 * hate this stuff. --Yufeng, 2025
	 */

	/* # of bytes per sector */
	lp->d_secsize = FVD_SECTOR_SIZE;

	/* # of sectors per track (S in CHS) */
	lp->d_nsectors = sc->sc_spt;

	/* # of tracks per cylinder (H in CHS) */
	lp->d_ntracks = sc->sc_heads;

	/* # of cylinders per disk (C in CHS) */
	lp->d_ncylinders = sc->sc_cylinders;

	/* # of sectors per cylinder */
	lp->d_secpercyl = lp->d_ntracks * lp->d_nsectors;

	/* # of sectors per disk */
	lp->d_secperunit = lp->d_secpercyl * lp->d_ncylinders;
	lp->d_secperunith = 0;

	lp->d_type = DTYPE_VND;
	strncpy(lp->d_typename, "FVD Image", sizeof(lp->d_typename));
	strncpy(lp->d_packname, "comp3301", sizeof(lp->d_packname));
	lp->d_version = 1;

	lp->d_magic = DISKMAGIC;
	lp->d_magic2 = DISKMAGIC;
	lp->d_checksum = dkcksum(lp);

	return (readdisklabel(DISKLABELDEV(dev), fvdstrategy, lp, spoofonly));
}

RBT_GENERATE(fvd_softcs, fvd_softc, sc_entry, fvd_cmp);
