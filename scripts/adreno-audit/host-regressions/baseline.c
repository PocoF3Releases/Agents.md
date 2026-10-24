// SPDX-License-Identifier: GPL-2.0-only
/*
 * Copyright (c) 2002,2007-2021, The Linux Foundation. All rights reserved.
 * Copyright (c) 2022-2023, Qualcomm Innovation Center, Inc. All rights reserved.
 */

/* Host-only fixture: external kernel operations are mocked. */
#include <stdint.h>
#include <stdio.h>
#include <errno.h>
#include <inttypes.h>
#define KGSL_MEMFLAGS_SPARSE_VIRT 1
#define KGSL_MEMFLAGS_SPARSE_PHYS 2
#define KGSL_MEMDESC_MAPPED 1
struct kgsl_memdesc {
    uint64_t gpuaddr, size, flags;
    unsigned priv;
};
struct kgsl_pagetable;
struct ops {
    int (*mmu_map)(struct kgsl_pagetable *, struct kgsl_memdesc *);
};
struct kgsl_pagetable {
    struct ops *pt_ops;
    struct {
        int entries;
        long mapped, max_mapped;
    } stats;
};
static int result;
static int map(struct kgsl_pagetable *p, struct kgsl_memdesc *m) {
    (void)p;
    (void)m;
    return result;
}
#define PT_OP_VALID(p, op) ((p)->pt_ops && (p)->pt_ops->op)
#define atomic_inc(p) (++*(p))
#define KGSL_STATS_ADD(s, c, m)                                                                    \
    do {                                                                                           \
        long value = (*(c) += (s));                                                                \
        if (value > *(m))                                                                          \
            *(m) = value;                                                                          \
    } while (0)
static int kgsl_memdesc_is_global(struct kgsl_memdesc *m) { return !!(m->flags & 4); }
static uint64_t kgsl_memdesc_footprint(struct kgsl_memdesc *m) { return m->size + 4096; }
int kgsl_mmu_map(struct kgsl_pagetable *pagetable, struct kgsl_memdesc *memdesc) {
    int size;

    if (!memdesc->gpuaddr)
        return -EINVAL;
    if (!(memdesc->flags & (KGSL_MEMFLAGS_SPARSE_VIRT | KGSL_MEMFLAGS_SPARSE_PHYS))) {
        /* Only global mappings should be mapped multiple times */
        if (!kgsl_memdesc_is_global(memdesc) && (KGSL_MEMDESC_MAPPED & memdesc->priv))
            return -EINVAL;
    }

    size = kgsl_memdesc_footprint(memdesc);

    if (PT_OP_VALID(pagetable, mmu_map)) {
        int ret;

        ret = pagetable->pt_ops->mmu_map(pagetable, memdesc);
        if (ret)
            return ret;

        atomic_inc(&pagetable->stats.entries);
        KGSL_STATS_ADD(size, &pagetable->stats.mapped, &pagetable->stats.max_mapped);

        /* This is needed for non-sparse mappings */
        memdesc->priv |= KGSL_MEMDESC_MAPPED;
    }

    return 0;
}
int main(void) {
    struct ops ops = {.mmu_map = map};
    uint64_t sizes[] = {65536, 0x7fffe000ULL, 0x7ffff000ULL, 0x80000000ULL, 0xfffff000ULL};
    int failures = 0;
    for (unsigned i = 0; i < sizeof(sizes) / sizeof(sizes[0]); i++) {
        struct kgsl_pagetable pt = {.pt_ops = &ops};
        struct kgsl_memdesc m = {.gpuaddr = 4096, .size = sizes[i]};
        result = 0;
        int rc = kgsl_mmu_map(&pt, &m);
        uint64_t expected = sizes[i] + 4096;
        int pass =
            rc == 0 && pt.stats.mapped == (long)expected && pt.stats.max_mapped == (long)expected;
        printf("%s size=0x%" PRIx64 " mapped=%ld expected=%" PRIu64 "\n", pass ? "PASS" : "FAIL",
               sizes[i], pt.stats.mapped, expected);
        if (!pass)
            failures++;
    }
    struct kgsl_pagetable pt = {.pt_ops = &ops};
    struct kgsl_memdesc m = {.gpuaddr = 4096, .size = 65536};
    result = -ENOMEM;
    int rc = kgsl_mmu_map(&pt, &m);
    int pass = rc == -ENOMEM && pt.stats.mapped == 0 && pt.stats.entries == 0 &&
               !(m.priv & KGSL_MEMDESC_MAPPED);
    printf("%s failed mapping leaves accounting unchanged\n", pass ? "PASS" : "FAIL");
    if (!pass)
        failures++;
    return failures ? 1 : 0;
}
