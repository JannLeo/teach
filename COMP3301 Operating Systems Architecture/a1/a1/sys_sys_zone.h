/*      $OpenBSD$       */

/*
 * Copyright (c) 2015 David Gwynne <dlg@uq.edu.au>
 * Copyright (c) 2025 Yufeng Gao <yufeng.gao@uq.edu.au>
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

#ifndef _SYS_ZONES_H_
#define _SYS_ZONES_H_

#include <sys/types.h>

#define MAXZONENAMELEN  256             /* max zone name length w/ NUL */
#define MAXZONES        1024
#define MAXZONEIDS      99999

struct zinfo {
        zoneid_t        zi_id;                          /* identifier */
        char            zi_name[MAXZONENAMELEN];        /* name */
        uid_t           zi_owner;                       /* owner */
        gid_t           zi_group;                       /* group */
        time_t          zi_ctime;                       /* creation time */
        int             zi_priority;                    /* sched priority */
};

#ifdef _KERNEL
void            zone_boot(void);
void            zone_bootdone(void);
int             zone_visible(struct process *, struct process *);
int             zone_authorise(struct proc *, struct zone *);
struct zone     *zone_ref(struct zone *);
void            zone_unref(struct zone *);
zoneid_t        zone_getid(const struct zone *);
struct zone     *zone_lookup(zoneid_t);
#endif

__BEGIN_DECLS
zoneid_t        zone_create(const char *);
int             zone_destroy(zoneid_t);
int             zone_enter(zoneid_t);
int             zone_list(zoneid_t *, size_t *);
int             zone_info(zoneid_t, struct zinfo *);
zoneid_t        zone_id(const char *);
int             zone_chown(zoneid_t, uid_t);
int             zone_chgrp(zoneid_t, gid_t);
__END_DECLS

#endif /* _SYS_ZONES_H_ */