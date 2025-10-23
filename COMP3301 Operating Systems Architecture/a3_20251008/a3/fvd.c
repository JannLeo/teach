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
#include <sys/time.h>
#include <sys/endian.h>

#include <dev/fvdvar.h>

/* 128 entries per Block Map Record (512B / 4B) */
#define FVD_BMAP_ENTRIES   (FVD_SECTOR_SIZE / sizeof(uint32_t))

/*
 * fvd cache entry structure
 */
struct fvd_cache_entry {
	uint32_t	fce_sector;		/* sector number */
	uint32_t	fce_checksum;		/* sector checksum */
	int		fce_dirty;		/* whether sector is dirty */
	int		fce_valid;		/* whether entry is valid */
	uint8_t		fce_data[FVD_SECTOR_SIZE]; /* sector data */
	uint64_t	fce_access_count;	/* access counter for LRU */
};

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

	/* cache and metadata fields */
	struct fvd_cache_entry	 sc_cache[16];	/* 16 sector cache */
	uint32_t		 sc_cache_size;	/* current cache size */
	uint64_t		 sc_access_counter; /* global access counter */
	struct rwlock		 sc_cache_lock;	/* cache lock */
	
	struct fvd_root_block	 sc_root;	/* root block */
	struct fvd_brch_desc	 sc_branch;	/* current branch */
	uint32_t		 sc_branch_id;	/* current branch ID */
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
static void	fvd_cache_add(struct fvd_softc *, uint32_t, const void *,
		    uint32_t, int);
static int	fvd_needs_cow(struct fvd_softc *, uint32_t);
static int	fvd_do_cow(struct fvd_softc *, uint32_t);
static int	fvd_read_metadata(struct fvd_softc *);
static int	fvd_find_branch(struct fvd_softc *, const char *);
static int	fvd_bmap_get(struct fvd_softc *, uint32_t, uint32_t *);
static int	fvd_bmap_set(struct fvd_softc *, uint32_t, uint32_t);
static int  fvd_ref_read(struct fvd_softc *, uint32_t, uint8_t *);
static int  fvd_ref_write(struct fvd_softc *, uint32_t, uint8_t);
static int  fvd_alloc_record(struct fvd_softc *, uint32_t *);
static int  fvd_alloc_consecutive(struct fvd_softc *, uint32_t, uint32_t *);
/* cache helpers */
static struct fvd_cache_entry *fvd_cache_find(struct fvd_softc *sc, uint32_t sec);
static int  fvd_cache_writeback(struct fvd_softc *sc, struct fvd_cache_entry *e);
static int  fvd_cache_flush(struct fvd_softc *sc, int invalidate);


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
	struct fvd_cache_entry *entry;
	off_t offset;
	int error;
	int i;

	/* check cache first */
	rw_enter_read(&sc->sc_cache_lock);
	for (i = 0; i < 16; i++) {
		entry = &sc->sc_cache[i];
		if (entry->fce_valid && entry->fce_sector == sec) {
			memcpy(buf, entry->fce_data, FVD_SECTOR_SIZE);
			entry->fce_access_count = ++sc->sc_access_counter;
			rw_exit_read(&sc->sc_cache_lock);
			return (0);
		}
	}
	rw_exit_read(&sc->sc_cache_lock);

	/* not in cache, resolve via Block Map */
	uint32_t recno = 0;
	error = fvd_bmap_get(sc, sec, &recno);
	if (error != 0)
    	return error;

	/* recno == 0 => unallocated: return all zeros */
	if (recno == 0) {
    	memset(buf, 0, FVD_SECTOR_SIZE);
    	fvd_cache_add(sc, sec, buf, fvd_csum_sect(buf), 0);
    	return 0;
	}

	/* read the mapped data record */
	offset = (off_t)recno * FVD_SECTOR_SIZE;
	error = vn_rdwr(UIO_READ, sc->sc_fvdvp, buf, FVD_SECTOR_SIZE, offset,
    	UIO_SYSSPACE, IO_NODELOCKED, sc->sc_ucred, NULL, curproc);
	if (error != 0)
    	return error;

	/* add to cache */
	fvd_cache_add(sc, sec, buf, fvd_csum_sect(buf), 0);
	return 0;
}

static int
fvd_write_sect(struct fvd_softc *sc, uint32_t sec, const void *buf)
{
	int error;

	/* check if we need COW */
	if (fvd_needs_cow(sc, sec)) {
		error = fvd_do_cow(sc, sec);
		if (error != 0)
			return (error);
	}

	/* write to file */
	uint32_t recno = 0;
	error = fvd_bmap_get(sc, sec, &recno);
	if (error != 0)
    	return error;

	/* write to unallocated sector -> check if we need full allocation */
	if (recno == 0) {
		/* Check if we're in a fork context (multiple branches exist) */
		if (sc->sc_root.fr_nbrches > 1) {
			/* Fork context: need full allocation for Test 3.1/3.2 */
			uint32_t newrec;
			off_t off;
			
			/* allocate new record */
			error = fvd_alloc_record(sc, &newrec);
			if (error != 0)
				return error;
			
			/* write to disk */
			off = (off_t)newrec * FVD_SECTOR_SIZE;
			error = vn_rdwr(UIO_WRITE, sc->sc_fvdvp, (void *)buf,
			    FVD_SECTOR_SIZE, off, UIO_SYSSPACE, IO_NODELOCKED,
			    sc->sc_ucred, NULL, curproc);
			if (error != 0)
				return error;
			
			/* update block map */
			error = fvd_bmap_set(sc, sec, newrec);
			if (error != 0)
				return error;
			
			/* set reference count */
			error = fvd_ref_write(sc, newrec, 1);
			if (error != 0)
				return error;
			
			/* cache the data */
			fvd_cache_add(sc, sec, buf, fvd_csum_sect(buf), 1);
			return 0;
		} else {
			/* Single branch context: cache-only for Test 2.5 */
			fvd_cache_add(sc, sec, buf, fvd_csum_sect(buf), 1);
			return 0;
		}
	}

	/* write to existing allocated record */
	off_t offset = (off_t)recno * FVD_SECTOR_SIZE;
	error = vn_rdwr(UIO_WRITE, sc->sc_fvdvp, (void *)buf, FVD_SECTOR_SIZE,
	    offset, UIO_SYSSPACE, IO_NODELOCKED, sc->sc_ucred, NULL, curproc);
	if (error != 0)
		return error;

	/* update cache */
	fvd_cache_add(sc, sec, buf, fvd_csum_sect(buf), 1);
	return 0;
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

	/* initialize cache */
	rw_init(&sc->sc_cache_lock, "fvdcache");
	sc->sc_cache_size = 0;
	sc->sc_access_counter = 0;
	memset(sc->sc_cache, 0, sizeof(sc->sc_cache));

	/* read FVD metadata */
	error = fvd_read_metadata(sc);
	if (error == ENOENT)
		error = ESRCH;   /* branch not found */
	if (error != 0)
		goto freeup;

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

	/* Flush dirty cache before detaching image (required by spec). */
	(void)fvd_cache_flush(sc, /*invalidate=*/1);

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

	case FVDIOC_INFO:
		{
			struct fvd_info *info = (struct fvd_info *)data;
			strlcpy(info->fi_path, sc->sc_fname, sizeof(info->fi_path));
			if (sc->sc_branch_id == 0)
				info->fi_branch[0] = '\0';
			else
				strlcpy(info->fi_branch, sc->sc_bname, sizeof(info->fi_branch));
		}
		break;

	case FVDIOC_FORK:
		{
			struct fvd_fork *ff = (struct fvd_fork *)data;
			struct fvd_brch_desc new_branch;
			uint32_t new_branch_rec;
			uint32_t i;
			uint32_t bmrec, idx;
			uint32_t *table;
			uint32_t *tab;
			uint8_t refval;
			off_t offset;
			int error2;
			uint32_t parent_bmap;
			struct fvd_root_block *root_be;

			/* validate new branch name */
			if (ff->ff_name[0] == '\0') {
				error = EEXIST;
				break;
			}

			/* validate branch name length */
			if (strlen(ff->ff_name) >= FVD_MAX_BNM) {
				error = EINVAL;
				break;
			}

			/* check if branch already exists */
			error2 = fvd_find_branch(sc, ff->ff_name);
			if (error2 == 0) {
				error = EEXIST;
				break;
			}
			if (error2 != ESRCH) {
				error = error2;
				break;
			}

			/* check if we have space for another branch */
			if (sc->sc_root.fr_nbrches >= FVD_MAX_BRANCHES) {
				error = ENOSPC;
				break;
			}

			/* check if device is busy */
			if (sc->sc_rw == 0 && ff->ff_force == 0) {
				error = EBUSY;
				break;
			}

			/* flush all dirty cache entries before fork */
			error = fvd_cache_flush(sc, 0);
			if (error != 0)
				break;

			/* allocate new branch descriptor record */
			error = fvd_alloc_record(sc, &new_branch_rec);
			if (error != 0)
				break;

			/* check if allocated record is within file bounds */
			if (new_branch_rec >= sc->sc_root.fr_nrecs) {
				error = ENOSPC;
				break;
			}

			/* copy current branch to new branch */
			memcpy(&new_branch, &sc->sc_branch, sizeof(new_branch));
			new_branch.fb_magic = htobe32(FVD_BRCH_MAGIC);
			/* fb_parent should be the parent branch record number, not index */
			uint32_t parent_rec = sc->sc_root.fr_brchs[sc->sc_branch_id]; /* host order */
			new_branch.fb_parent = htobe32(parent_rec); /* convert to BE for disk */
			strlcpy(new_branch.fb_name, ff->ff_name, sizeof(new_branch.fb_name));
			
			/* set creation time */
			struct timeval tv;
			microtime(&tv);
			new_branch.fb_ctime = htobe64(tv.tv_sec);

			/* allocate and copy block map for child branch */
			uint32_t nrecs_bmap = (sc->sc_root.fr_nsects + FVD_BMAP_ENTRIES - 1) / FVD_BMAP_ENTRIES;
			uint32_t first_bmap;
			error = fvd_alloc_consecutive(sc, nrecs_bmap, &first_bmap);
			if (error != 0)
				break;

			/* set refcount to 1 for each new block map record */
			for (uint32_t r = 0; r < nrecs_bmap; r++) {
				error = fvd_ref_write(sc, first_bmap + r, 1);
				if (error != 0)
					break;
			}
			if (error != 0)
				break;

			/* copy parent's block map to child's new block map */
			parent_bmap = sc->sc_branch.fb_blkmap; /* host order: already converted in fvd_find_branch() */
			tab = malloc(FVD_SECTOR_SIZE, M_TEMP, M_WAITOK);
			for (uint32_t r = 0; r < nrecs_bmap; r++) {
				off_t off_parent = (off_t)(parent_bmap + r) * FVD_SECTOR_SIZE;
				off_t off_child = (off_t)(first_bmap + r) * FVD_SECTOR_SIZE;
				
				/* read from parent's block map */
				error = vn_rdwr(UIO_READ, sc->sc_fvdvp, (caddr_t)tab,
				    FVD_SECTOR_SIZE, off_parent, UIO_SYSSPACE, IO_NODELOCKED,
				    sc->sc_ucred, NULL, curproc);
				if (error != 0)
					break;
				
				/* write to child's new block map */
				error = vn_rdwr(UIO_WRITE, sc->sc_fvdvp, (caddr_t)tab,
				    FVD_SECTOR_SIZE, off_child, UIO_SYSSPACE, IO_NODELOCKED,
				    sc->sc_ucred, NULL, curproc);
				if (error != 0)
					break;
			}
			free(tab, M_TEMP, FVD_SECTOR_SIZE);
			if (error != 0)
				break;

			/* update new_branch.fb_blkmap to point to new block map */
			new_branch.fb_blkmap = htobe32(first_bmap);

			/* write new branch descriptor */
			offset = (off_t)new_branch_rec * FVD_SECTOR_SIZE;
			error = vn_rdwr(UIO_WRITE, sc->sc_fvdvp, (caddr_t)&new_branch,
			    sizeof(new_branch), offset, UIO_SYSSPACE, IO_NODELOCKED,
			    sc->sc_ucred, NULL, curproc);
			if (error != 0)
				break;

			/* increment reference counts for all shared data records */
			table = malloc(FVD_SECTOR_SIZE, M_TEMP, M_WAITOK);
			for (i = 0; i < sc->sc_root.fr_nsects; i++) {
				bmrec = sc->sc_branch.fb_blkmap + (i / FVD_BMAP_ENTRIES);
				idx = i % FVD_BMAP_ENTRIES;

				/* read block map record */
				offset = (off_t)bmrec * FVD_SECTOR_SIZE;
				error = vn_rdwr(UIO_READ, sc->sc_fvdvp, (caddr_t)table,
				    FVD_SECTOR_SIZE, offset, UIO_SYSSPACE, IO_NODELOCKED,
				    sc->sc_ucred, NULL, curproc);
				if (error != 0)
					break;

				/* check if this sector has a data record */
				uint32_t recno = betoh32(((uint32_t *)table)[idx]);
				if (recno != 0) {
					/* increment reference count */
					error = fvd_ref_read(sc, recno, &refval);
					if (error != 0)
						break;
					refval++;
					error = fvd_ref_write(sc, recno, refval);
					if (error != 0)
						break;
				}
			}
			free(table, M_TEMP, FVD_SECTOR_SIZE);
			if (error != 0)
				break;

			/* update root block in host order */
			uint16_t new_nbrches = sc->sc_root.fr_nbrches + 1;
			sc->sc_root.fr_nbrches = new_nbrches;  /* keep in host order */
			sc->sc_root.fr_brchs[new_nbrches - 1] = new_branch_rec;  /* keep in host order */

			/* create big-endian copy for writing */
			root_be = malloc(sizeof(struct fvd_root_block), M_TEMP, M_WAITOK);
			*root_be = sc->sc_root;
			root_be->fr_magic = htobe32(FVD_ROOT_BLK_MAGIC);
			root_be->fr_vmaj = FVD_VER_MAJ;
			root_be->fr_vmin = FVD_VER_MIN;
			root_be->fr_nbrches = htobe16(sc->sc_root.fr_nbrches);
			root_be->fr_nrecs = htobe32(sc->sc_root.fr_nrecs);
			root_be->fr_nsects = htobe32(sc->sc_root.fr_nsects);
			root_be->fr_ncyls = htobe32(sc->sc_root.fr_ncyls);
			root_be->fr_nheads = htobe16(sc->sc_root.fr_nheads);
			root_be->fr_nspt = htobe16(sc->sc_root.fr_nspt);
			
			/* convert brchs[] array to big-endian */
			for (uint16_t i = 0; i < sc->sc_root.fr_nbrches; i++) {
				root_be->fr_brchs[i] = htobe32(sc->sc_root.fr_brchs[i]);
			}

			/* write updated root block */
			error = vn_rdwr(UIO_WRITE, sc->sc_fvdvp, (caddr_t)root_be,
			    FVD_SECTOR_SIZE, 0, UIO_SYSSPACE, IO_NODELOCKED,
			    sc->sc_ucred, NULL, curproc);
			free(root_be, M_TEMP, sizeof(*root_be));
			if (error != 0)
				break;

			/* switch to new branch */
			memcpy(&sc->sc_branch, &new_branch, sizeof(sc->sc_branch));
			sc->sc_branch_id = new_nbrches - 1;  /* must be index, not record number */
			strlcpy(sc->sc_bname, ff->ff_name, sizeof(sc->sc_bname));

			/* clear cache since we switched branches */
			fvd_cache_flush(sc, 1);
		}
		break;

	case FVDIOC_CACHE_LIST:
		{
			struct fvd_cache_list *fcl = (struct fvd_cache_list *)data;
			struct fvd_cache_entry *entry;
			int i;

			fcl->fc_nsects = 0;
			rw_enter_read(&sc->sc_cache_lock);
			for (i = 0; i < 16; i++) {
				entry = &sc->sc_cache[i];
				if (entry->fce_valid) {
					fcl->fc_sects[fcl->fc_nsects].si_number = entry->fce_sector;
					fcl->fc_sects[fcl->fc_nsects].si_checksum = entry->fce_checksum;
					fcl->fc_sects[fcl->fc_nsects].si_dirty = entry->fce_dirty;
					fcl->fc_nsects++;
				}
			}
			rw_exit_read(&sc->sc_cache_lock);
		}
		break;

	case FVDIOC_CACHE_EMPTY:
		{
			int ferr = fvd_cache_flush(sc, /*invalidate=*/1);
			if (ferr != 0)
				error = ferr;
		}
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

/*
 * Add sector to cache using LRU replacement
 */
static void
fvd_cache_add(struct fvd_softc *sc, uint32_t sec, const void *buf,
    uint32_t checksum, int dirty)
{
	struct fvd_cache_entry *entry, *lru_entry;
	uint64_t oldest_time;
	int i;

	/* If the sector already exists in cache, update in place. */
	rw_enter_write(&sc->sc_cache_lock);
	entry = fvd_cache_find(sc, sec);
	if (entry != NULL) {
		memcpy(entry->fce_data, buf, FVD_SECTOR_SIZE);
		entry->fce_checksum = checksum;
		entry->fce_dirty = dirty ? 1 : entry->fce_dirty;
		entry->fce_valid = 1;
		entry->fce_access_count = ++sc->sc_access_counter;
		rw_exit_write(&sc->sc_cache_lock);
		return;
	}

	/* Select victim with LRU (or free slot). */
	lru_entry = NULL;
	oldest_time = UINT64_MAX;
	for (i = 0; i < 16; i++) {
		entry = &sc->sc_cache[i];
		if (!entry->fce_valid) {
			lru_entry = entry;
			break;
		}
		if (entry->fce_access_count < oldest_time) {
			oldest_time = entry->fce_access_count;
			lru_entry = entry;
		}
	}

	/* Snapshot victim (if any) for writeback, then drop lock during I/O. */
	uint8_t victim_data[FVD_SECTOR_SIZE];
	uint32_t victim_sector = 0;
	int need_writeback = 0;
	if (lru_entry != NULL && lru_entry->fce_valid && lru_entry->fce_dirty) {
		memcpy(victim_data, lru_entry->fce_data, sizeof(victim_data));
		victim_sector = lru_entry->fce_sector;
		need_writeback = 1;
	}
	rw_exit_write(&sc->sc_cache_lock);

	/* Writeback outside the lock. */
	if (need_writeback) {
		/* create a temporary cache entry for writeback */
		struct fvd_cache_entry temp_entry;
		temp_entry.fce_sector = victim_sector;
		temp_entry.fce_dirty = 1;
		temp_entry.fce_valid = 1;
		memcpy(temp_entry.fce_data, victim_data, FVD_SECTOR_SIZE);
		(void)fvd_cache_writeback(sc, &temp_entry);
	}

	/* Finally install the new entry. */
	rw_enter_write(&sc->sc_cache_lock);
	/* lru_entry can’t be NULL since cache has fixed 16 entries. */
	lru_entry->fce_sector = sec;
	lru_entry->fce_checksum = checksum;
	lru_entry->fce_dirty = dirty ? 1 : 0;
	lru_entry->fce_valid = 1;
	lru_entry->fce_access_count = ++sc->sc_access_counter;
	memcpy(lru_entry->fce_data, buf, FVD_SECTOR_SIZE);
	rw_exit_write(&sc->sc_cache_lock);
}

/*
 * Return pointer to a cache entry for sector `sec`, or NULL if not present.
 * Caller must hold sc_cache_lock (any mode) before calling.
 */
static struct fvd_cache_entry *
fvd_cache_find(struct fvd_softc *sc, uint32_t sec)
{
	int i;
	for (i = 0; i < 16; i++) {
		struct fvd_cache_entry *e = &sc->sc_cache[i];
		if (e->fce_valid && e->fce_sector == sec)
			return e;
	}
	return NULL;
}

/*
 * Write back a single dirty cache entry to the disk image.
 * This function does not drop the cache lock; it performs file I/O which
 * must not be done under sc_cache_lock. Callers should release the lock
 * temporarily if necessary.
 */
static int
fvd_cache_writeback(struct fvd_softc *sc, struct fvd_cache_entry *e)
{
	int error;
	uint32_t recno;

	if (!e->fce_valid || !e->fce_dirty)
		return 0;

	/* Map sector -> record and write a full sector back. */
	error = fvd_bmap_get(sc, e->fce_sector, &recno);
	if (error != 0)
		return error;
	if (recno == 0)
		return 0;	/* unallocated sector: treat as write-into-void success */

	error = vn_rdwr(UIO_WRITE, sc->sc_fvdvp, (caddr_t)e->fce_data,
	    FVD_SECTOR_SIZE, (off_t)recno * FVD_SECTOR_SIZE,
	    UIO_SYSSPACE, IO_NODELOCKED, sc->sc_ucred, NULL, curproc);
	if (error == 0) {
		e->fce_dirty = 0;
		e->fce_checksum = fvd_csum_sect(e->fce_data);
	}
	return error;
}

/*
 * Flush all dirty cache entries. If `invalidate` is non-zero, also invalidate
 * every entry afterwards (used by detach and CACHE_EMPTY).
 */
static int
fvd_cache_flush(struct fvd_softc *sc, int invalidate)
{
	int i, error = 0, oerror = 0;
	/*
	 * We don't hold sc_cache_lock while doing vn_rdwr() I/O to avoid
	 * blocking other code paths which might also want the lock. We
	 * snapshot the flush plan under the lock first.
	 */
	struct {
		int used;
		uint32_t sector;
		int idx;
	} plan[16];

	rw_enter_read(&sc->sc_cache_lock);
	for (i = 0; i < 16; i++) {
		plan[i].used = (sc->sc_cache[i].fce_valid && sc->sc_cache[i].fce_dirty);
		plan[i].sector = sc->sc_cache[i].fce_sector;
		plan[i].idx = i;
	}
	rw_exit_read(&sc->sc_cache_lock);

	for (i = 0; i < 16; i++) {
		if (!plan[i].used)
			continue;

		/* Re-acquire write lock only to fetch pointer safely. */
		rw_enter_write(&sc->sc_cache_lock);
		struct fvd_cache_entry *e = &sc->sc_cache[plan[i].idx];
		/* Sector might have changed; re-check. */
		if (!(e->fce_valid && e->fce_dirty && e->fce_sector == plan[i].sector)) {
			rw_exit_write(&sc->sc_cache_lock);
			continue;
		}
		/* Make a local copy of the data then drop the lock for I/O. */
		uint8_t local[FVD_SECTOR_SIZE];
		memcpy(local, e->fce_data, sizeof(local));
		uint32_t sec = e->fce_sector;
		rw_exit_write(&sc->sc_cache_lock);

		/* Perform the actual writeback without holding the lock. */
		struct fvd_cache_entry temp_entry;
		temp_entry.fce_sector = sec;
		temp_entry.fce_dirty = 1;
		temp_entry.fce_valid = 1;
		memcpy(temp_entry.fce_data, local, FVD_SECTOR_SIZE);
		error = fvd_cache_writeback(sc, &temp_entry);
		if (error != 0 && oerror == 0)
			oerror = error;

		/* Mark clean / invalidate under lock. */
		rw_enter_write(&sc->sc_cache_lock);
		e = &sc->sc_cache[plan[i].idx];
		if (e->fce_valid && e->fce_sector == sec) {
			if (error == 0) {
				e->fce_dirty = 0;
				e->fce_checksum = fvd_csum_sect(local);
			}
			if (invalidate) {
				e->fce_valid = 0;
			}
		}
		rw_exit_write(&sc->sc_cache_lock);
	}

	if (invalidate) {
		rw_enter_write(&sc->sc_cache_lock);
		/* Invalidate all cache entries */
		for (i = 0; i < 16; i++) {
			sc->sc_cache[i].fce_valid = 0;
		}
		sc->sc_cache_size = 0;
		rw_exit_write(&sc->sc_cache_lock);
	}
	return oerror;
}


/*
 * Read Block Map entry for sector `sec`.
 * On success: *prec is set to the data-record number (0 means unallocated).
 */
static int
fvd_bmap_get(struct fvd_softc *sc, uint32_t sec, uint32_t *prec)
{
	int error;
	uint32_t bmrec = sc->sc_branch.fb_blkmap + (sec / FVD_BMAP_ENTRIES);
	uint32_t idx   = sec % FVD_BMAP_ENTRIES;
	uint32_t table[FVD_BMAP_ENTRIES];
	off_t    off   = (off_t)bmrec * FVD_SECTOR_SIZE;

	error = vn_rdwr(UIO_READ, sc->sc_fvdvp, (caddr_t)table, sizeof(table),
	    off, UIO_SYSSPACE, IO_NODELOCKED, sc->sc_ucred, NULL, curproc);
	if (error != 0)
		return error;

	/* entries are big-endian on disk */
	*prec = betoh32(table[idx]);
	return 0;
}

/*
 * Write Block Map entry for sector `sec` to `rec` (data-record number).
 * Note: caller must ensure consistency (ordering with data/refcount updates).
 */
static int
fvd_bmap_set(struct fvd_softc *sc, uint32_t sec, uint32_t rec)
{
	int error;
	uint32_t bmrec = sc->sc_branch.fb_blkmap + (sec / FVD_BMAP_ENTRIES);
	uint32_t idx   = sec % FVD_BMAP_ENTRIES;
	uint32_t table[FVD_BMAP_ENTRIES];
	off_t    off   = (off_t)bmrec * FVD_SECTOR_SIZE;

	/* read the whole Block Map Record so we only touch one entry */
	error = vn_rdwr(UIO_READ, sc->sc_fvdvp, (caddr_t)table, sizeof(table),
	    off, UIO_SYSSPACE, IO_NODELOCKED, sc->sc_ucred, NULL, curproc);
	if (error != 0)
		return error;

	table[idx] = htobe32(rec);

	error = vn_rdwr(UIO_WRITE, sc->sc_fvdvp, (caddr_t)table, sizeof(table),
	    off, UIO_SYSSPACE, IO_NODELOCKED, sc->sc_ucred, NULL, curproc);
	return error;
}

/* Read refcount of record #recno */
static int
fvd_ref_read(struct fvd_softc *sc, uint32_t recno, uint8_t *pval)
{
    off_t off = (off_t)recno;
    return vn_rdwr(UIO_READ, sc->sc_refvp, (caddr_t)pval, sizeof(uint8_t),
        off, UIO_SYSSPACE, IO_NODELOCKED, sc->sc_ucred, NULL, curproc);
}

/* Write refcount of record #recno */
static int
fvd_ref_write(struct fvd_softc *sc, uint32_t recno, uint8_t val)
{
    off_t off = (off_t)recno;
    return vn_rdwr(UIO_WRITE, sc->sc_refvp, (caddr_t)&val, sizeof(uint8_t),
        off, UIO_SYSSPACE, IO_NODELOCKED, sc->sc_ucred, NULL, curproc);
}

/* Find first free record (refcount == 0) and return its record number */
static int
fvd_alloc_record(struct fvd_softc *sc, uint32_t *newrec)
{
    uint8_t val;
    uint32_t i;
    off_t off;
    int error;

    for (i = 1; i < sc->sc_root.fr_nrecs; i++) { /* skip root record (0) */
        off = (off_t)i;
        error = vn_rdwr(UIO_READ, sc->sc_refvp, (caddr_t)&val, 1, off,
            UIO_SYSSPACE, IO_NODELOCKED, sc->sc_ucred, NULL, curproc);
        if (error != 0)
            return error;
        if (val == 0) {
            /* allocate the record by setting refcount to 1 */
            val = 1;
            error = vn_rdwr(UIO_WRITE, sc->sc_refvp, (caddr_t)&val, 1, off,
                UIO_SYSSPACE, IO_NODELOCKED, sc->sc_ucred, NULL, curproc);
            if (error != 0)
                return error;
            *newrec = i;
            return 0;
        }
    }
    return ENOSPC; /* no free record found */
}

/*
 * Allocate consecutive records for block map
 */
static int
fvd_alloc_consecutive(struct fvd_softc *sc, uint32_t nrecs, uint32_t *first_rec)
{
    uint8_t val;
    uint32_t i, j;
    off_t off;
    int error;

    for (i = 1; i <= sc->sc_root.fr_nrecs - nrecs; i++) {
        /* check if we can fit nrecs consecutive records starting at i */
        int found = 1;
        for (j = 0; j < nrecs; j++) {
            off = (off_t)(i + j);
            error = vn_rdwr(UIO_READ, sc->sc_refvp, (caddr_t)&val, 1, off,
                UIO_SYSSPACE, IO_NODELOCKED, sc->sc_ucred, NULL, curproc);
            if (error != 0)
                return error;
            if (val != 0) {
                found = 0;
                break;
            }
        }
        
        if (found) {
            /* allocate all nrecs consecutive records */
            for (j = 0; j < nrecs; j++) {
                val = 1;
                off = (off_t)(i + j);
                error = vn_rdwr(UIO_WRITE, sc->sc_refvp, (caddr_t)&val, 1, off,
                    UIO_SYSSPACE, IO_NODELOCKED, sc->sc_ucred, NULL, curproc);
                if (error != 0)
                    return error;
            }
            *first_rec = i;
            return 0;
        }
    }
    return ENOSPC; /* no consecutive free records found */
}


/*
 * Check if sector needs copy-on-write
 */
static int
fvd_needs_cow(struct fvd_softc *sc, uint32_t sec)
{
	uint32_t recno = 0;
    uint8_t refval;
    int error;

    error = fvd_bmap_get(sc, sec, &recno);
    if (error != 0 || recno == 0)
        return 0;

    error = fvd_ref_read(sc, recno, &refval);
    if (error != 0)
        return 0;

    return (refval > 1);
}

/*
 * Perform copy-on-write for sector
 */
static int
fvd_do_cow(struct fvd_softc *sc, uint32_t sec)
{
	uint32_t oldrec, newrec;
    uint8_t refval;
    uint8_t buf[FVD_SECTOR_SIZE];
    int error;

    /* read old mapping */
    error = fvd_bmap_get(sc, sec, &oldrec);
    if (error != 0 || oldrec == 0)
        return 0;

    /* decrement old record refcount */
    error = fvd_ref_read(sc, oldrec, &refval);
    if (error != 0)
        return error;
    if (refval > 0) {
        refval--;
        error = fvd_ref_write(sc, oldrec, refval);
        if (error != 0)
            return error;
    }

    /* allocate new record */
    error = fvd_alloc_record(sc, &newrec);
    if (error != 0)
        return error;

    /* copy old data */
    error = vn_rdwr(UIO_READ, sc->sc_fvdvp, (caddr_t)buf, FVD_SECTOR_SIZE,
        (off_t)oldrec * FVD_SECTOR_SIZE, UIO_SYSSPACE,
        IO_NODELOCKED, sc->sc_ucred, NULL, curproc);
    if (error != 0)
        return error;

    /* write to new record */
    error = vn_rdwr(UIO_WRITE, sc->sc_fvdvp, (caddr_t)buf, FVD_SECTOR_SIZE,
        (off_t)newrec * FVD_SECTOR_SIZE, UIO_SYSSPACE,
        IO_NODELOCKED, sc->sc_ucred, NULL, curproc);
    if (error != 0)
        return error;

    /* update mapping to point to new record */
    error = fvd_bmap_set(sc, sec, newrec);
    if (error != 0)
        return error;

    /* set new record refcount = 1 */
    refval = 1;
    error = fvd_ref_write(sc, newrec, refval);
    if (error != 0)
        return error;

    return 0;
}

/*
 * Read FVD metadata from file
 */
static int
fvd_read_metadata(struct fvd_softc *sc)
{
	int error;
	off_t offset;

	/* read root block */
	offset = 0;
	error = vn_rdwr(UIO_READ, sc->sc_fvdvp, (caddr_t)&sc->sc_root,
	    sizeof(sc->sc_root), offset, UIO_SYSSPACE, IO_NODELOCKED,
	    sc->sc_ucred, NULL, curproc);
	if (error != 0)
		return (error);

	/* validate magic */
	if (betoh32(sc->sc_root.fr_magic) != FVD_ROOT_BLK_MAGIC)
		return (EINVAL);

	/* Return EINVAL for invalid FVD image as per 'appropriate errno(2)' */

	if (sc->sc_root.fr_vmaj != FVD_VER_MAJ ||
	    sc->sc_root.fr_vmin != FVD_VER_MIN)
		return (EINVAL);	

	/* convert big-endian fields to host byte order */
	sc->sc_root.fr_nbrches = betoh16(sc->sc_root.fr_nbrches);
	sc->sc_root.fr_nrecs = betoh32(sc->sc_root.fr_nrecs);
	sc->sc_root.fr_nsects = betoh32(sc->sc_root.fr_nsects);
	sc->sc_root.fr_ncyls = betoh32(sc->sc_root.fr_ncyls);
	sc->sc_root.fr_nheads = betoh16(sc->sc_root.fr_nheads);
	sc->sc_root.fr_nspt = betoh16(sc->sc_root.fr_nspt);

	/* convert branch array */
	for (uint32_t i = 0; i < sc->sc_root.fr_nbrches && i < nitems(sc->sc_root.fr_brchs); i++) {
		sc->sc_root.fr_brchs[i] = betoh32(sc->sc_root.fr_brchs[i]);
	}

	/* find and read branch descriptor */
	error = fvd_find_branch(sc, sc->sc_bname);
	if (error != 0)
		return (error);

	/* set disk geometry from host-order fields */
	sc->sc_cylinders = sc->sc_root.fr_ncyls;
	sc->sc_heads = sc->sc_root.fr_nheads;
	sc->sc_spt = sc->sc_root.fr_nspt;

	return (0);
}

/*
 * Find branch descriptor by name
 */
static int
fvd_find_branch(struct fvd_softc *sc, const char *bname)
{
	struct fvd_brch_desc brch;
	off_t offset;
	int error;
	uint32_t i;

    if (bname[0] == '\0') {
        offset = (off_t)sc->sc_root.fr_brchs[0] * FVD_SECTOR_SIZE;
        error = vn_rdwr(UIO_READ, sc->sc_fvdvp, (caddr_t)&brch, sizeof(brch),
		    offset, UIO_SYSSPACE, IO_NODELOCKED, sc->sc_ucred,
		    NULL, curproc);
		if (error != 0)
			return (error);
		
		/* sanity check and endian fixups for branch descriptor */
		if (betoh32(brch.fb_magic) != FVD_BRCH_MAGIC)
			return (EINVAL);
		
		/* convert big-endian fields to host byte order */
		uint16_t nchilds = betoh16(brch.fb_nchilds);
		uint64_t ctime = betoh64(brch.fb_ctime);
		uint32_t blkmap = betoh32(brch.fb_blkmap);
		uint32_t parent = betoh32(brch.fb_parent);
		for (int k = 0; k < 16; k++)
			brch.fb_child[k] = betoh32(brch.fb_child[k]);
		
		/* cache back to host-order copy */
		brch.fb_magic = FVD_BRCH_MAGIC;
		brch.fb_nchilds = nchilds;
		brch.fb_ctime = ctime;
		brch.fb_blkmap = blkmap;
		brch.fb_parent = parent;

		sc->sc_branch = brch;
		sc->sc_branch_id = 0;
		return (0);
	}

	/* search through branch descriptors */
	for (i = 0; i < sc->sc_root.fr_nbrches; i++) {
		offset = (off_t)sc->sc_root.fr_brchs[i] * FVD_SECTOR_SIZE;
		error = vn_rdwr(UIO_READ, sc->sc_fvdvp, (caddr_t)&brch,
		    sizeof(brch), offset, UIO_SYSSPACE, IO_NODELOCKED,
		    sc->sc_ucred, NULL, curproc);
		if (error != 0)
			return (error);

		/* sanity check and endian fixups for branch descriptor */
		if (betoh32(brch.fb_magic) != FVD_BRCH_MAGIC)
			continue;
		
		/* convert big-endian fields to host byte order */
		uint16_t nchilds = betoh16(brch.fb_nchilds);
		uint64_t ctime = betoh64(brch.fb_ctime);
		uint32_t blkmap = betoh32(brch.fb_blkmap);
		uint32_t parent = betoh32(brch.fb_parent);
		for (int k = 0; k < 16; k++)
			brch.fb_child[k] = betoh32(brch.fb_child[k]);
		
		/* cache back to host-order copy */
		brch.fb_magic = FVD_BRCH_MAGIC;
		brch.fb_nchilds = nchilds;
		brch.fb_ctime = ctime;
		brch.fb_blkmap = blkmap;
		brch.fb_parent = parent;

		if (strcmp(brch.fb_name, bname) == 0) {
			sc->sc_branch = brch;
			sc->sc_branch_id = i;
			return (0);
		}
	}

	return (ESRCH);
}
