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

#include <sys/zones.h>
#include <sys/types.h>
#include <sys/wait.h>

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
#include <err.h>
#include <errno.h>
#include <pwd.h>
#include <grp.h>
#include <limits.h>

#ifndef nitems
#define nitems(_a) (sizeof(_a) / sizeof(_a[0]))
#endif

struct task {
        const char *name;
        int (*task)(int, char *[]);
        const char *usage;
};

static const char zcreate_usage[] = "create zonename";
static int      zcreate(int, char *[]);

static const char zdestroy_usage[] = "destroy zonename";
static int      zdestroy(int, char *[]);

static const char zexec_usage[] = "exec zonename command ...";
static int      zexec(int, char *[]);

static const char zid_usage[] = "id [zonename]";
static int      zid(int, char *[]);

static const char zlist_usage[] = "list";
static int      zlist(int, char *[]);

static const char zchown_usage[] = "chown zonename user";
static int      zchown(int, char *[]);

static const char zchgrp_usage[] = "chgrp zonename group";
static int      zchgrp(int, char *[]);

static const struct task tasks[] = {
        { "create",     zcreate,        zcreate_usage },
        { "destroy",    zdestroy,       zdestroy_usage },
        { "exec",       zexec,          zexec_usage },
        { "id",         zid,            zid_usage },
        { "list",       zlist,          zlist_usage },
        { "chown",      zchown,         zchown_usage },
        { "chgrp",      zchgrp,         zchgrp_usage }
};

static const struct task *
task_lookup(const char *arg)
{
        const struct task *t;
        size_t i;

        for (i = 0; i < nitems(tasks); i++) {
                t = &tasks[i];
                if (strcmp(arg, t->name) == 0)
                        return (t);
        }

        return (NULL);
}

__dead void
usage(void)
usage(void)
{
        extern char *__progname;
        const struct task *t;
        size_t i;

        fprintf(stderr, "usage:");
        for (i = 0; i < nitems(tasks); i++) {
                t = &tasks[i];
                fprintf(stderr, "\t%s %s\n", __progname, t->usage);
        }

        exit(1);
}

__dead void
zusage(const char *str)
{
        extern char *__progname;

        fprintf(stderr, "usage: %s %s\n", __progname, str);

        exit(1);
}

int
main(int argc, char *argv[])
{
        const struct task *t;

        if (argc < 2)
                usage();

        t = task_lookup(argv[1]);
        if (t == NULL)
                usage();

        argc -= 1;
        argv += 1;

        return (t->task(argc, argv));
}

static zoneid_t
getzoneid(const char *zone)
{
        const char *errstr;
        zoneid_t z;

        z = zone_id(zone);
        if (z == -1) {
                if (errno != ESRCH)
                        err(1, "zone lookup");

                z = strtonum(zone, 0, MAXZONEIDS, &errstr);
                if (errstr != NULL)
                        errx(1, "unknown zone \"%s\"", zone);
        }

        return (z);
}

static int
zcreate(int argc, char *argv[])
{
        if (argc != 2)
                zusage(zcreate_usage);

        if (zone_create(argv[1]) == -1)
                err(1, "create");

        return (0);
}

static int
zdestroy(int argc, char *argv[])
{
        zoneid_t z;

        if (argc != 2)
                zusage(zdestroy_usage);

        z = getzoneid(argv[1]);

        if (zone_destroy(z) == -1)
                err(1, "destroy");

        return (0);
}

static int
zexec(int argc, char *argv[])
{
        zoneid_t z;

        if (argc < 3)
                zusage(zexec_usage);

        z = getzoneid(argv[1]);

        if (zone_enter(z) == -1)
                err(1, "enter");

        execvp(argv[2], &argv[2]);

        err(1, "exec %s", argv[2]);
        /* NOTREACHED */
}

static int
zid(int argc, char *argv[])
{
        const char *zonename;
        zoneid_t z;

        switch (argc) {
        case 1:
                zonename = NULL;
                break;
        case 2:
                zonename = argv[1];
                break;
        default:
                zusage(zid_usage);
        }

        z = zone_id(zonename);
        if (z == -1)
                err(1, "id");

        printf("%d\n", z);

        return (0);
}

static int
zlist(int argc, char *argv[])
{
        struct zinfo info;
        zoneid_t *zs = NULL;
        size_t nzs, i = 8;
        zoneid_t z;

        if (argc != 1)
                zusage(zlist_usage);

        for (;;) {
                nzs = i;

                zs = reallocarray(zs, nzs, sizeof(*zs));
                if (zs == NULL)
                        err(1, "lookup");

                if (zone_list(zs, &nzs) == 0)
                        break;

                if (errno != EFAULT && errno != ERANGE)
                        err(1, "list");

                i <<= 1;
        }

        printf("%8s %s\n", "ID", "NAME");

        for (i = 0; i < nzs; i++) {
                z = zs[i];
                if (zone_info(z, &info) == -1)
                        err(1, "info");
                printf("%8d %s\n", z, info.zi_name);
        }

        free(zs);

        return (0);
}

static int
zchown(int argc, char *argv[])
{
        zoneid_t z;
        uid_t uid;
        const char *errstr;

        if (argc != 3)
                zusage(zchown_usage);

        z = getzoneid(argv[1]);
        if (uid_from_user(argv[2], &uid) == -1) {
                uid = strtonum(argv[2], 0, UID_MAX, &errstr);
                if (errstr != NULL)
                        errx(1, "chown: invalid user");
        }

        if (zone_chown(z, uid) == -1)
                err(1, "chown");

        return (0);
}

static int
zchgrp(int argc, char *argv[])
{
        zoneid_t z;
        gid_t gid;
        const char *errstr;

        if (argc != 3)
                zusage(zchgrp_usage);

        z = getzoneid(argv[1]);
        if (gid_from_group(argv[2], &gid) == -1) {
                gid = strtonum(argv[2], 0, GID_MAX, &errstr);
                if (errstr != NULL)
                        errx(1, "chgrp: invalid group");
        }

        if (zone_chgrp(z, gid) == -1)
                err(1, "chgrp");

        return (0);
}