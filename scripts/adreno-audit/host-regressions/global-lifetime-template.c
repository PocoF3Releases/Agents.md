// SPDX-License-Identifier: GPL-2.0-only
/*
 * Copyright (c) 2002,2007-2021, The Linux Foundation. All rights reserved.
 * Copyright (c) 2022-2023, Qualcomm Innovation Center, Inc. All rights reserved.
 * Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
 * Host fixture: actual KGSL functions, external operations mocked.
 */
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
typedef uint64_t u64;
typedef int64_t s64;
#define PAGE_SHIFT 12
#define KGSL_MEMDESC_GLOBAL 2
#define KGSL_MEMDESC_MAPPED 4
#define KGSL_MEMFLAGS_SPARSE_VIRT 1
#define KGSL_MEMFLAGS_SPARSE_PHYS 2
struct kgsl_memdesc {
    u64 size, gpuaddr, flags;
    unsigned priv;
};
struct kgsl_mmu {
    int unused;
};
struct kgsl_device {
    struct kgsl_mmu mmu;
    int64_t total;
};
struct kgsl_pagetable;
struct ops {
    int (*mmu_map)(struct kgsl_pagetable *, struct kgsl_memdesc *);
    int (*mmu_unmap)(struct kgsl_pagetable *, struct kgsl_memdesc *);
};
struct kgsl_pagetable {
    struct kgsl_mmu *mmu;
    struct ops *pt_ops;
    struct {
        int entries;
        long mapped, max_mapped;
    } stats;
};
static struct kgsl_device gpu;
#define KGSL_MMU_DEVICE(mmu) ((void)(mmu), &gpu)
#define KGSL_IOMMU_GLOBAL_MEM_BASE(mmu) ((void)(mmu), 4096ULL)
#define PT_OP_VALID(pt, op) ((pt)->pt_ops && (pt)->pt_ops->op)
#define atomic_inc(x) (++*(x))
#define atomic_dec(x) (--*(x))
#define atomic_long_sub(n, x) (*(x) -= (n))
#define KGSL_STATS_ADD(n, x, m)                                                                    \
    do {                                                                                           \
        *(x) += (n);                                                                               \
        if (*(x) > *(m))                                                                           \
            *(m) = *(x);                                                                           \
    } while (0)
static int map_result;
static int mapping(struct kgsl_pagetable *p, struct kgsl_memdesc *m) {
    (void)p;
    (void)m;
    return map_result;
}
static bool kgsl_memdesc_is_global(const struct kgsl_memdesc *m) {
    return m->priv & KGSL_MEMDESC_GLOBAL;
}
static bool kgsl_memdesc_is_dmabuf(const struct kgsl_memdesc *m) { return !!(m->flags & 128); }
static u64 kgsl_memdesc_footprint(const struct kgsl_memdesc *m) { return m->size + 4096; }
static void kgsl_mmu_trace_gpu_mem_pagetable(struct kgsl_pagetable *p) { (void)p; }
static void kgsl_trace_gpu_mem_total(struct kgsl_device *d, int64_t size) { d->total += size; }
static struct {
    struct kgsl_memdesc *memdesc;
} global_pt_entries[1];
static int global_pt_count = 1;
static int global_map;
#define bitmap_clear(map, offset, size)                                                            \
    do {                                                                                           \
        (void)(map);                                                                               \
        (void)(offset);                                                                            \
        (void)(size);                                                                              \
    } while (0)
/* DRIVER_FUNCTIONS */
static int failures;
#define CHECK(cond, name)                                                                          \
    do {                                                                                           \
        printf("%s %s\n", (cond) ? "PASS" : "FAIL", name);                                         \
        if (!(cond))                                                                               \
            failures++;                                                                            \
    } while (0)
int main(void) {
    struct ops ops = {mapping, mapping};
    struct kgsl_pagetable a = {.mmu = &gpu.mmu, .pt_ops = &ops}, b = a;
    struct kgsl_memdesc m = {.size = 65536, .gpuaddr = 4096, .priv = KGSL_MEMDESC_GLOBAL};
    global_pt_entries[0].memdesc = &m;
    kgsl_mmu_map(&a, &m);
    kgsl_mmu_map(&b, &m);
    CHECK(gpu.total == 69632, "global counted once across two pagetables");
    kgsl_mmu_unmap(&a, &m);
    kgsl_mmu_unmap(&b, &m);
    CHECK(gpu.total == 69632 && a.stats.mapped == 0 && b.stats.mapped == 0,
          "pagetable teardown retains global accounting");
    kgsl_iommu_remove_global(&gpu.mmu, &m);
    CHECK(gpu.total == 0, "final global release balances counter");
    gpu.total = 0;
    kgsl_iommu_remove_global(&gpu.mmu, &m);
    CHECK(gpu.total == 0, "repeated removal does not subtract twice");
    m = (struct kgsl_memdesc){.size = 65536, .gpuaddr = 4096, .priv = KGSL_MEMDESC_GLOBAL};
    global_pt_entries[0].memdesc = &m;
    map_result = -ENOMEM;
    CHECK(kgsl_mmu_map(&a, &m) == -ENOMEM, "failed global map rejected");
    kgsl_iommu_remove_global(&gpu.mmu, &m);
    CHECK(gpu.total == 0, "never-mapped global cannot underflow");
    m = (struct kgsl_memdesc){.size = 65536, .gpuaddr = 4096, .priv = KGSL_MEMDESC_GLOBAL};
    global_pt_entries[0].memdesc = &m;
    map_result = 0;
    kgsl_mmu_map(&a, &m);
    global_pt_entries[0].memdesc = NULL;
    kgsl_iommu_remove_global(&gpu.mmu, &m);
    CHECK(gpu.total == 69632, "unrecognized descriptor does not decrement");
    global_pt_entries[0].memdesc = &m;
    kgsl_mmu_unmap(&a, &m);
    kgsl_iommu_remove_global(&gpu.mmu, &m);
    CHECK(gpu.total == 0, "later successful removal balances counter");
    return failures ? 1 : 0;
}
