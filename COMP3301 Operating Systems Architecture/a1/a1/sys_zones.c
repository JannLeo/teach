/*      $OpenBSD$       */

/*
 * Copyright (c) 2015, 2023 David Gwynne <dlg@uq.edu.au>
 * Copyright (c) 2024 Lachlan Tinsley <l.tinsley@uq.edu.au>
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

#include <sys/param.h>
#include <sys/systm.h>
#include <sys/proc.h>
#include <sys/zones.h>

#include <sys/socket.h>
#include <sys/mount.h>
#include <sys/syscallargs.h>

#include <sys/types.h>
#include <sys/errno.h>

#include <sys/malloc.h>
#include <sys/pool.h>
#include <sys/rwlock.h>
#include <sys/atomic.h>
#include <sys/tree.h>

struct zone {
        zoneid_t         z_id;
        struct refcnt    z_refs;
        char            *z_name;
        size_t           z_namelen;
        struct rwlock    z_lock;
        uid_t            z_uid;
        gid_t            z_gid;
        time_t           z_ctime;

        RBT_ENTRY(zone)  z_nm_entry;
        RBT_ENTRY(zone)  z_id_entry;
};

static struct zone zone_global = {
        .z_id           = 0,
        .z_refs         = REFCNT_INITIALIZER(),
        .z_name         = "global",
        .z_lock         = RWLOCK_INITIALIZER("zone"),
        .z_uid          = 0,
        .z_gid          = 0
};

struct zone * const global_zone = &zone_global;

RBT_HEAD(zone_id_tree, zone);
RBT_HEAD(zone_nm_tree, zone);

struct zones {
        struct rwlock           zs_lock;
        struct zone_id_tree     zs_id_tree;
        struct zone_nm_tree     zs_nm_tree;
        struct pool             zs_pool;
};

static struct zones zones = {
        .zs_lock        = RWLOCK_INITIALIZER("zones"),
        .zs_id_tree     = RBT_INITIALIZER(&zones.zs_id_tree),
        .zs_nm_tree     = RBT_INITIALIZER(&zones.zs_nm_tree),
};

static inline int
zone_id_cmp(const struct zone *a, const struct zone *b)
{
        if (a->z_id < b->z_id)
                return (-1);
        if (a->z_id > b->z_id)
                return (1);
        return (0);
}

RBT_PROTOTYPE(zone_id_tree, zone, z_id_entry, zone_id_cmp);

static inline int
zone_nm_cmp(const struct zone *a, const struct zone *b)
{
        return (strcmp(a->z_name, b->z_name));
}

RBT_PROTOTYPE(zone_nm_tree, zone, z_nm_entry, zone_nm_cmp);

int     zone_global_list(zoneid_t **, size_t *);

void
zone_boot(void)
{
        pool_init(&zones.zs_pool, sizeof(struct zone), 0, IPL_NONE, PR_WAITOK,
            "zonepl", NULL);
        pool_sethardlimit(&zones.zs_pool, MAXZONES - 1,
            "zones limit reached", 1);

        global_zone->z_namelen = strlen(global_zone->z_name) + 1;
        /* the trees own the references */
        RBT_INSERT(zone_id_tree, &zones.zs_id_tree, global_zone);
        RBT_INSERT(zone_nm_tree, &zones.zs_nm_tree, global_zone);
}

void
zone_bootdone(void)
{
        /* things to do after bootup is mostly done */
        global_zone->z_ctime = gettime();
}

struct zone *
zone_lookup(zoneid_t z)
{
        struct zone key;
        struct zone *zone;

        key.z_id = z;

        rw_enter_read(&zones.zs_lock);
        zone = RBT_FIND(zone_id_tree, &zones.zs_id_tree, &key);
        if (zone != NULL)
                zone_ref(zone);
        rw_exit_read(&zones.zs_lock);

        return (zone);
}

struct zone *
zone_ref(struct zone *zone)
{
        refcnt_take(&zone->z_refs);
        return (zone);
}

void
zone_unref(struct zone *zone)
{
        int last = refcnt_rele(&zone->z_refs);
        if (last)
                panic("%s: last zone %p reference released", __func__, zone);
}

int
zone_visible(struct process *self, struct process *target)
{
        struct zone *zone = self->ps_zone;

        return (zone == global_zone || zone == target->ps_zone);
}

zoneid_t
zone_getid(const struct zone *zone)
{
        return (zone->z_id);
}

int
zone_authorise(struct proc *p, struct zone *zone)
{
        int rv = EPERM;

        rw_enter_read(&zone->z_lock);

        if (!suser(p) || groupmember(zone->z_gid, p->p_ucred) ||
            zone->z_uid == p->p_ucred->cr_uid)
                rv = 0;

        rw_exit_read(&zone->z_lock);

        return rv;
}

int
sys_zone_create(struct proc *p, void *v, register_t *retval)
{
        struct sys_zone_create_args /* {
                syscallarg(const char *) zonename;
        } */ *uap = v;
        struct zone *zone;
        char zonename[MAXZONENAMELEN];
        size_t zonenamelen;
        int rv;

        *retval = -1;

        if (p->p_p->ps_zone != global_zone)
                return (EPERM);

        rv = copyinstr(SCARG(uap, zonename), zonename, sizeof(zonename),
            &zonenamelen);
        if (rv != 0)
                return (rv);

        zone = pool_get(&zones.zs_pool, PR_WAITOK | PR_LIMITFAIL);
        if (zone == NULL)
                return (ERANGE);

        refcnt_init(&zone->z_refs); /* starts at 1 */
        zone->z_namelen = zonenamelen;
        zone->z_name = malloc(zone->z_namelen, M_DEVBUF, M_WAITOK);
        memcpy(zone->z_name, zonename, zone->z_namelen);
        zone->z_uid = p->p_ucred->cr_uid;
        zone->z_gid = p->p_ucred->cr_gid;
        zone->z_ctime = gettime();
        rw_init(&zone->z_lock, "zlock");

        rv = rw_enter(&zones.zs_lock, RW_WRITE|RW_INTR);
        if (rv != 0)
                goto free;

        if (RBT_INSERT(zone_nm_tree, &zones.zs_nm_tree, zone) != NULL) {
                rw_exit(&zones.zs_lock);
                rv = EEXIST;
                goto free;
        }

        do {
                zone->z_id = arc4random_uniform(MAXZONEIDS);
        } while (RBT_INSERT(zone_id_tree, &zones.zs_id_tree, zone) != NULL);

        *retval = zone->z_id;
        rw_exit(&zones.zs_lock);

        return (0);

free:
        free(zone->z_name, M_DEVBUF, zone->z_namelen);
        pool_put(&zones.zs_pool, zone);
        return (rv);
}

int
sys_zone_destroy(struct proc *p, void *v, register_t *retval)
{
        struct sys_zone_destroy_args /* {
                syscallarg(zoneid_t) z;
        } */ *uap = v;
        struct zone key;
        struct zone *zone;
        int rv;

        *retval = -1;
        if (p->p_p->ps_zone != global_zone)
                return (EPERM);

        key.z_id = SCARG(uap, z);

        rw_enter_write(&zones.zs_lock);
        zone = RBT_FIND(zone_id_tree, &zones.zs_id_tree, &key);
        if (zone == NULL) {
                rv = ESRCH;
                goto fail;
        }

        if (zone_authorise(p, zone)) {
                rv = EPERM;
                goto fail;
        }

        if (!refcnt_rele_last(&zone->z_refs)) {
                rv = EBUSY;
                goto fail;
        }

        RBT_REMOVE(zone_nm_tree, &zones.zs_nm_tree, zone);
        RBT_REMOVE(zone_id_tree, &zones.zs_id_tree, zone);
        rw_exit_write(&zones.zs_lock);

        free(zone->z_name, M_DEVBUF, zone->z_namelen);
        pool_put(&zones.zs_pool, zone);

        *retval = 0;
        return (0);
fail:
        rw_exit_write(&zones.zs_lock);
        return (rv);
}

int
sys_zone_enter(struct proc *p, void *v, register_t *retval)
{
        struct sys_zone_enter_args /* {
                syscallarg(zoneid_t) z;
        } */ *uap = v;
        struct zone *zone;

        *retval = -1;
        if (p->p_p->ps_zone != global_zone)
                return (EPERM);

        zone = zone_lookup(SCARG(uap, z));
        if (zone == NULL)
                return (ESRCH);

        if (zone_authorise(p, zone)) {
                zone_unref(zone);
                return (EPERM);
        }

        if (atomic_cas_ptr(&p->p_p->ps_zone, global_zone, zone) !=
            global_zone) {
                zone_unref(zone);
                return (EPERM);
        }
        /* we're giving the zone_lookup ref to this process */

        zone_unref(global_zone); /* drop gz ref */

        *retval = 0;
        return (0);
}

int
zone_global_list(zoneid_t **zsp, size_t *nzsp)
{
        struct zone *zone;
        zoneid_t *zs;
        size_t nzs;
        size_t i = 0;

        /* sneaking info off the pool is naughty */
        nzs = zones.zs_pool.pr_nout + 1; /* count the gz */
        if (nzs > *nzsp)
                return (ERANGE);

        zs = mallocarray(nzs, sizeof(*zs), M_TEMP, M_WAITOK);

        RBT_FOREACH(zone, zone_id_tree, &zones.zs_id_tree)
                zs[i++] = zone->z_id;

        KASSERT(i == nzs);

        *zsp = zs;
        *nzsp = nzs;

        return (0);
}

int
sys_zone_list(struct proc *p, void *v, register_t *retval)
{
        struct sys_zone_list_args /* {
                syscallarg(zoneid_t *) zs;
                syscallarg(size_t *) nzs;
        } */ *uap = v;

        struct zone *zone;
        zoneid_t *zs;
        zoneid_t *zsp = SCARG(uap, zs);
        size_t nzs;
        size_t *nzsp = SCARG(uap, nzs);
        int rv;

        *retval = -1;

        zone = p->p_p->ps_zone;

        rv = copyin(nzsp, &nzs, sizeof(nzs));
        if (rv != 0)
                return (rv);

        if (zone == global_zone) {
                rw_enter_read(&zones.zs_lock);
                rv = zone_global_list(&zs, &nzs);
                rw_exit_read(&zones.zs_lock);
                if (rv != 0)
                        return (rv);

                rv = copyout(zs, zsp, nzs * sizeof(zoneid_t));
                free(zs, M_TEMP, nzs * sizeof(zoneid_t));
                if (rv != 0)
                        return (rv);
        } else {
                if (nzs < 1)
                        return (ERANGE);
                nzs = 1;
                rv = copyout(&zone->z_id, zsp, sizeof(zoneid_t));
                if (rv != 0)
                        return (rv);
        }

        rv = copyout(&nzs, nzsp, sizeof(nzs));
        if (rv != 0)
                return (rv);

        *retval = 0;
        return (0);
}

int
sys_zone_info(struct proc *p, void *v, register_t *retval)
{
        struct sys_zone_info_args /* {
                syscallarg(zoneid_t) z;
                syscallarg(struct zinfo *) info;
        } */ *uap = v;
        struct zone *zone;
        struct zinfo zi;
        zoneid_t z;
        int rv;

        *retval = -1;
        memset(&zi, 0xCC, sizeof(zi));

        zone = p->p_p->ps_zone;
        z = SCARG(uap, z);

        if (zone == global_zone) {
                zone = zone_lookup(z);
                if (zone == NULL)
                        return (ESRCH);
        } else if (zone->z_id != z)
                return (ESRCH);
        else
                zone_ref(zone);

        zi.zi_id = z;
        memcpy(&zi.zi_name, zone->z_name, zone->z_namelen);
        rw_enter_read(&zone->z_lock);
        zi.zi_owner = zone->z_uid;
        zi.zi_group = zone->z_gid;
        rw_exit_read(&zone->z_lock);
        zi.zi_ctime = zone->z_ctime;

        rv = copyout(&zi, SCARG(uap, info), sizeof(zi));
        zone_unref(zone);
        if (rv != 0)
                return (EFAULT);

        *retval = 0;
        return (0);
}

int
sys_zone_id(struct proc *p, void *v, register_t *retval)
{
        struct sys_zone_id_args /* {
                syscallarg(const char *) zonename;
        } */ *uap = v;
        char zonename[MAXZONENAMELEN];
        size_t zonenamelen;
        struct zone *zone;
        struct zone key = { .z_name = zonename };
        int rv;

        zone = p->p_p->ps_zone;

        /* NULL zone name means current zone */
        if (SCARG(uap, zonename) == NULL) {
                *retval = zone->z_id;
                return (0);
        }

        *retval = -1;

        rv = copyinstr(SCARG(uap, zonename), zonename,
            sizeof(zonename), &zonenamelen);
        if (rv != 0)
                return (rv);

        /* shortcuts for non-gz */
        if (zone != global_zone) {
                if (strcmp(zone->z_name, zonename) != 0)
                        return (ESRCH);

                *retval = zone->z_id;
                return (0);
        }

        rv = rw_enter(&zones.zs_lock, RW_READ|RW_INTR);
        if (rv != 0)
                return (rv);

        zone = RBT_FIND(zone_nm_tree, &zones.zs_nm_tree, &key);
        if (zone == NULL)
                rv = ESRCH;
        else
                *retval = zone->z_id;

        rw_exit(&zones.zs_lock);

        return (rv);
}

int
sys_zone_chown(struct proc *p, void *v, register_t *retval)
{
        struct sys_zone_chown_args /* {
                syscallarg(zoneid_t) z;
                syscallarg(uid_t) user;
        } */ *uap = v;
        struct zone *zone;
        zoneid_t z;

        *retval = -1;

        zone = p->p_p->ps_zone;
        z = SCARG(uap, z);

        if (zone == global_zone) {
                zone = zone_lookup(z);
                if (zone == NULL)
                        return (ESRCH);
        } else if (zone->z_id != z)
                return (ESRCH);
        else
                zone_ref(zone);

        if (zone == global_zone || zone_authorise(p, zone)) {
                zone_unref(zone);
                return (EPERM);
        }

        rw_enter_write(&zone->z_lock);
        zone->z_uid = SCARG(uap, user);
        rw_exit_write(&zone->z_lock);
        *retval = 0;

        zone_unref(zone);
        return (0);
}

int
sys_zone_chgrp(struct proc *p, void *v, register_t *retval)
{
        struct sys_zone_chgrp_args /* {
                syscallarg(zoneid_t) z;
                syscallarg(gid_t) group;
        } */ *uap = v;
        struct zone *zone;
        zoneid_t z;

        *retval = -1;

        zone = p->p_p->ps_zone;
        z = SCARG(uap, z);

        if (zone == global_zone) {
                zone = zone_lookup(z);
                if (zone == NULL)
                        return (ESRCH);
        } else if (zone->z_id != z)
                return (ESRCH);
        else
                zone_ref(zone);

        if (zone == global_zone || zone_authorise(p, zone)) {
                zone_unref(zone);
                return (EPERM);
        }

        rw_enter_write(&zone->z_lock);
        zone->z_gid = SCARG(uap, group);
        rw_exit_write(&zone->z_lock);
        *retval = 0;

        zone_unref(zone);
        return (0);
}

RBT_GENERATE(zone_id_tree, zone, z_id_entry, zone_id_cmp);
RBT_GENERATE(zone_nm_tree, zone, z_nm_entry, zone_nm_cmp);