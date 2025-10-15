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

#include <sys/ioctl.h>

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <limits.h>
#include <errno.h>
#include <ctype.h>
#include <inttypes.h>
#include <err.h>

#include <dev/fvdvar.h>

#ifndef nitems
#define nitems(_a) ((sizeof((_a)) / sizeof((_a)[0])))
#endif

#define FVD_PREFIX	"fvd"
#define FVD_PREFIXLEN	(sizeof(FVD_PREFIX) - 1)

struct subcmd {
	int (*cmd)(const struct subcmd *, int, char *[]);
	const char *name;
	const char *usage;
};

static int	fvd_attach(const struct subcmd *, int, char *[]);
static int	fvd_detach(const struct subcmd *, int, char *[]);
static int	fvd_info(const struct subcmd *, int, char *[]);
static int	fvd_fork(const struct subcmd *, int, char *[]);
static int	fvd_io(const struct subcmd *, int, char *[]);

static const struct subcmd subcmds[] = {
	{ fvd_attach,	"attach",
	    "[-Dr] fvdX image.fvd [branch]" },
	{ fvd_detach,	"detach",
	    "[-Df] fvdX" },
	{ fvd_info,	"info",
	    "[-D] fvdX" },
	{ fvd_fork,	"fork",
	    "[-Df] fvdX name" },
	{ fvd_io,	"io",
	    "[-D] fvdX [script]"},
};

static const struct subcmd *
		fvd_subcmd_lookup(const char *);

__dead static void
usage(void)
{
	extern char *__progname;
	const struct subcmd *c = &subcmds[0];
	size_t i;

	fprintf(stderr, "usage:\t%s %s", __progname, c->name);
	for (i = 1; i < nitems(subcmds); i++) {
		c = &subcmds[i];
		printf("|%s", c->name);
	}
	printf(" ...\n");

	for (i = 0; i < nitems(subcmds); i++) {
		c = &subcmds[i];
		fprintf(stderr, "\t%s %s %s\n", __progname,
		    c->name, c->usage);
	}

	exit(1);
}

__dead static void
fvd_usage(const struct subcmd *c)
{
	extern char *__progname;

	fprintf(stderr, "\t%s fvdX %s %s\n", __progname,
	    c->name, c->usage);

	exit(1);
}

int
main(int argc, char *argv[])
{
	const struct subcmd *c;

	if (argc < 2)
		usage();

	argc -= 1;
	argv += 1;

	c = fvd_subcmd_lookup(argv[0]);
	if (c == NULL) {
		warnx("unknown command %s", argv[0]);
		usage();
	}

	return (*c->cmd)(c, argc, argv);
}

static const struct subcmd *
fvd_subcmd_lookup(const char *name)
{
	size_t i;

	for (i = 0; i < nitems(subcmds); i++) {
		const struct subcmd *c = &subcmds[i];
		if (strcmp(c->name, name) == 0)
			return (c);
	}

	return (NULL);
}

static int
openfvd(int Dflag, const char *name, int flags)
{
	char dpath[PATH_MAX];
	size_t namelen;
	const char *errstr;
	int rv;
	int dfd;

	if (!Dflag) {
		namelen = strlen(name);
		if (namelen < FVD_PREFIXLEN)
			errx(1, "%s: short name", name);
		if (memcmp(name, FVD_PREFIX, FVD_PREFIXLEN) != 0) {
			errx(1, "%s: invalid %s device name prefix", name,
			    FVD_PREFIX);
		}

		(void)strtonum(name + FVD_PREFIXLEN, 0, 0xffffffff, &errstr);
		if (errstr != NULL)
			errx(1, "%s: unit number: %s", name, errstr);

		rv = snprintf(dpath, sizeof(dpath), "/dev/r%sc", name);
		if (rv == -1 || (size_t)rv >= sizeof(dpath))
			errx(1, "devpath snprintf");

		name = dpath;
	}

	dfd = open(name, flags);
	if (dfd == -1)
		err(1, "%s", name);

	return dfd;
}

static int
fvd_attach(const struct subcmd *c, int argc, char *argv[])
{
	struct fvd_attach fa = {
		.fa_readonly = 0,
	};
	int Dflag = 0;
	int ch;
	int dfd;

	while ((ch = getopt(argc, argv, "Dr")) != -1) {
		switch (ch) {
		case 'D':
			Dflag = 1;
			break;
		case 'r':
			fa.fa_readonly = 1;
			break;
		default:
			fvd_usage(c);
			/* NOTREACHED */
		}
	}

	argc -= optind;
	argv += optind;

	if (argc < 2 || argc > 3)
		fvd_usage(c);

	dfd = openfvd(Dflag, argv[0], O_RDWR);
	fa.fa_path = argv[1];
	fa.fa_branch = (argc == 3) ? argv[2] : "";

	if (ioctl(dfd, FVDIOC_ATTACH, &fa) == -1)
		err(1, "%s %s %s %s", c->name, argv[0], argv[1], argv[2] ?
		    argv[2] : "[default]");

	return (0);
}

static int
fvd_detach(const struct subcmd *c, int argc, char *argv[])
{
	int force = 0;
	int Dflag = 0;
	int ch;
	int dfd;

	while ((ch = getopt(argc, argv, "Df")) != -1) {
		switch (ch) {
		case 'D':
			Dflag = 1;
			break;
		case 'f':
			force = 1;
			break;
		default:
			fvd_usage(c);
			/* NOTREACHED */
		}
	}

	argc -= optind;
	argv += optind;

	if (argc != 1)
		fvd_usage(c);

	dfd = openfvd(Dflag, argv[0], O_RDWR);

	if (ioctl(dfd, FVDIOC_DETACH, &force) == -1)
		err(1, "%s%s %s", force ? "force " : "", c->name, argv[0]);

	return (0);
}

static int
fvd_info(const struct subcmd *c, int argc, char *argv[])
{
	struct fvd_info info;
	int Dflag = 0;
	int ch;
	int dfd;

	while ((ch = getopt(argc, argv, "D")) != -1) {
		switch (ch) {
		case 'D':
			Dflag = 1;
			break;
		default:
			fvd_usage(c);
			/* NOTREACHED */
		}
	}

	argc -= optind;
	argv += optind;

	if (argc != 1)
		fvd_usage(c);

	dfd = openfvd(Dflag, argv[0], O_RDONLY);

	if (ioctl(dfd, FVDIOC_INFO, &info) == -1)
		err(1, "%s %s", c->name, argv[0]);

	printf("FVD image: %s\n", info.fi_path);
	printf("Branch: %s\n", info.fi_branch[0] ? info.fi_branch :
	    "default");

	return (0);
}

static int
fvd_fork(const struct subcmd *c, int argc, char *argv[])
{
	struct fvd_fork ff;
	int force = 0;
	int Dflag = 0;
	int ch;
	int dfd;

	while ((ch = getopt(argc, argv, "Df")) != -1) {
		switch (ch) {
		case 'D':
			Dflag = 1;
			break;
		case 'f':
			force = 1;
			break;
		default:
			fvd_usage(c);
			/* NOTREACHED */
		}
	}

	argc -= optind;
	argv += optind;

	if (argc != 2)
		fvd_usage(c);

	dfd = openfvd(Dflag, argv[0], O_RDWR);
	strlcpy(ff.ff_name, argv[1], sizeof(ff.ff_name));
	ff.ff_force = force;

	if (ioctl(dfd, FVDIOC_FORK, &ff) == -1)
		err(1, "%s%s %s %s", force ? "force " : "", c->name, argv[0],
		    argv[1]);

	return (0);
}

static char *
ltrim(char *str)
{
	while (isspace((unsigned char)*str))
		str++;
	return str;
}

static char *
rtrim(char *str)
{
	char *end = str + strlen(str) - 1;
	while (end >= str && isspace((unsigned char)*end)) {
		*end = '\0';
		end--;
	}
	return str;
}

static int
cmp_sects(const void *a, const void *b)
{
	const struct sec_info *sa = (const struct sec_info *)a;
	const struct sec_info *sb = (const struct sec_info *)b;

	if (sa->si_number < sb->si_number)
		return (-1);
	else if (sa->si_number > sb->si_number)
		return (1);
	else
		return (0);
}

static void
sort_cache_list(struct fvd_cache_list *fcl)
{
	qsort(fcl->fc_sects, fcl->fc_nsects, sizeof(struct sec_info),
	    cmp_sects);
}

static uint32_t
checksum(const void *buf)
{
	const uint8_t *data = buf;
	uint32_t sum1 = 0xFFFF, sum2 = 0xFFFF;

	for (size_t i = 0; i < FVD_SECTOR_SIZE; i++) {
		sum1 = (sum1 + data[i]) % 0xFFFF;
		sum2 = (sum2 + sum1) % 0xFFFF;
	}

	return (sum2 << 16) | sum1;
}


static int
fvd_io(const struct subcmd *c, int argc, char *argv[])
{
	int Dflag = 0;
	int ch;
	int dfd;
	FILE *fp;
	char *line, *p, wch;
	size_t len, n, i;
	uint32_t sec;
	char buf[FVD_SECTOR_SIZE];
	struct fvd_cache_list fcl;

	while ((ch = getopt(argc, argv, "D")) != -1) {
		switch (ch) {
		case 'D':
			Dflag = 1;
			break;
		default:
			fvd_usage(c);
			/* NOTREACHED */
		}
	}

	argc -= optind;
	argv += optind;

	if (argc < 1 || argc > 3)
		fvd_usage(c);

	dfd = openfvd(Dflag, argv[0], O_RDWR);

	fp = argv[1] ? fopen(argv[1], "r") : stdin;
	if (!fp)
		err(1, "%s %s %s", c->name, argv[0], argv[1]);

	if (isatty(fileno(fp))) {
		printf("supported commands:\n");
		printf("  r <sector>        - reads a sector and prints "
		    "checksum\n");
		printf("  w <sector> <char> - writes a sector filled with "
		    "<char> and prints checksum of written data\n");
		printf("  e                 - empties the sector cache\n");
		printf("  l                 - lists the sectors currently "
		    "in cache\n");
		printf("  q                 - quits\n");
		if (isatty(fileno(stdout))) {
			printf("\n> ");
			fflush(stdout);
		}
	}

	line = NULL;
	n = 0;
	while (getline(&line, &len, fp) != -1) {
		n++;
		p = rtrim(ltrim(line));

		if (*p == '\0' || *p == '#')
			continue;

		switch (*p) {
		case 'r':
			if (sscanf(p, "r %"PRIu32, &sec) != 1) {
				warnx("line %zu: invalid read command", n);
				break;
			}
			if (pread(dfd, buf, sizeof(buf), (off_t)sec *
			    FVD_SECTOR_SIZE) != sizeof(buf)) {
				warnx("line %zu: reading sector %"PRIu32" "
				    "failed", n, sec);
				break;
			}
			printf("line %zu: read sector %"PRIu32" - csum = "
			    "0x%08"PRIX32"\n", n, sec, checksum(buf));
			break;
		case 'w':
			if (sscanf(p, "w %"PRIu32" %c", &sec, &wch) != 2) {
				warnx("line %zu: invalid write command", n);
				break;
			}
			memset(buf, (unsigned char)wch, sizeof(buf));
			if (pwrite(dfd, buf, sizeof(buf), (off_t)sec *
			    FVD_SECTOR_SIZE) != sizeof(buf)) {
				warnx("line %zu: writing sector %"PRIu32" "
				    "failed", n, sec);
				break;
			}
			printf("line %zu: written sector %"PRIu32" - csum = "
			    "0x%08"PRIX32"\n", n, sec, checksum(buf));
			break;
		case 'e':
			if (ioctl(dfd, FVDIOC_CACHE_EMPTY, NULL) == -1) {
				warnx("line %zu: failed to empty cache", n);
				break;
			}
			printf("line %zu: sector cache emptied\n", n);
			break;
		case 'l':
			if (ioctl(dfd, FVDIOC_CACHE_LIST, &fcl) == -1) {
				warnx("line %zu: failed to list cache", n);
				break;
			}
			printf("line %zu: %zu sectors currently in cache:\n",
			    n, fcl.fc_nsects);
			sort_cache_list(&fcl);
			for (i = 0; i < fcl.fc_nsects; i++)
				printf("  %9"PRIu32"\t0x%08"PRIX32"%s\n",
				    fcl.fc_sects[i].si_number,
				    fcl.fc_sects[i].si_checksum,
				    fcl.fc_sects[i].si_dirty ? "\tdirty" : "");
			break;
		case 'q':
			exit(0);
			/* NOTREACHED */
		default:
			warnx("line %zu: invalid command \"%c\"", n, *p);
			break;
		}

		if (isatty(fileno(fp)) && isatty(fileno(stdout))) {
			printf("> ");
			fflush(stdout);
		}
	}

	return (0);
}
