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

#ifndef _DEV_FVDVAR_H_
#define _DEV_FVDVAR_H_

/*
 * fvd definitions
 */

#define FVD_SECTOR_SIZE		512

/*
 * fvd root block structure
 */
struct fvd_root_block {
#define FVD_ROOT_BLK_MAGIC	0x46564449
	uint32_t	fr_magic;
#define FVD_VER_MAJ		1
	uint8_t		fr_vmaj;
#define FVD_VER_MIN		0
	uint8_t		fr_vmin;
	uint16_t	fr_nbrches;
	uint32_t	fr_nrecs;
	uint32_t	fr_nsects;
#define FVD_MAX_CYLINDERS	0x10000
	uint32_t	fr_ncyls;
#define FVD_MAX_HEADS		16
	uint16_t	fr_nheads;
#define FVD_MAX_SPT		255
	uint16_t	fr_nspt;
#define FVD_MAX_BRANCHES	122
	uint32_t	fr_brchs[FVD_MAX_BRANCHES];
} __packed;

/*
 * fvd branch descriptor format
 */
struct fvd_brch_desc {
#define FVD_BRCH_MAGIC		0x42524348	/* branch desciptor magic */
	uint32_t	fb_magic;
	uint16_t	fb_nchilds;
	uint64_t	fb_ctime;
	uint32_t	fb_blkmap;
	uint32_t	fb_parent;
#define FVD_MAX_CHILDS		16		/* max number of childs */
	uint32_t	fb_child[FVD_MAX_CHILDS];
#define FVD_MAX_BNM		32		/* max branch name length */
	char		fb_name[FVD_MAX_BNM];
	uint8_t		fb_padding[394];
} __packed;

/*
 * ioctl interface
 */

struct fvd_attach {
	const char	*fa_path;	/* path to FVD image */
	const char	*fa_branch;	/* branch to attach */
	int		 fa_readonly;	/* whether to attach as read-only */
};

struct fvd_info {
	char	fi_path[1024];		/* path to attached FVD image */
	char	fi_branch[FVD_MAX_BNM];	/* current branch name */
};

struct fvd_fork {
	char	ff_name[FVD_MAX_BNM];	/* new branch name */
	int	ff_force;		/* forced fork */
};

struct sec_info {
	uint32_t	si_number;	/* sector number */
	uint32_t	si_checksum;	/* sector checksum */
	int		si_dirty;	/* whether sector is dirty */
};

struct fvd_cache_list {
	size_t		fc_nsects;	/* number of sectors in cache */
	struct sec_info	fc_sects[16];	/* info about cached sectors */
};


#define FVDIOC_ATTACH		_IOW('F', 1, struct fvd_attach)
#define FVDIOC_DETACH		_IOW('F', 2, int)
#define FVDIOC_INFO		_IOR('F', 3, struct fvd_info)
#define FVDIOC_FORK		_IOW('F', 4, struct fvd_fork)
#define FVDIOC_CACHE_LIST	_IOR('F', 5, struct fvd_cache_list)
#define FVDIOC_CACHE_EMPTY	_IO('F', 6)

#endif /* _DEV_FVDVAR_H */
