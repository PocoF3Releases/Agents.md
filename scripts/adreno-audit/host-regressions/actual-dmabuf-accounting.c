// SPDX-License-Identifier: GPL-2.0-only
/*
 * Copyright (c) 2008-2021, The Linux Foundation. All rights reserved.
 * Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
 */

/* Host-only fixture: external kernel operations are mocked. */
#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
typedef uint64_t u64;
typedef int64_t s64;
struct list_head {
    struct list_head *next, *prev;
};
#define INIT_LIST_HEAD(p)                                                                          \
    do {                                                                                           \
        (p)->next = (p);                                                                           \
        (p)->prev = (p);                                                                           \
    } while (0)
static void list_add(struct list_head *n, struct list_head *h) {
    n->next = h->next;
    n->prev = h;
    h->next->prev = n;
    h->next = n;
}
static void list_del(struct list_head *n) {
    n->prev->next = n->next;
    n->next->prev = n->prev;
}
static int list_empty(struct list_head *h) { return h->next == h; }
#define container_of(p, t, m) ((t *)((char *)(p) - offsetof(t, m)))
#define list_for_each_entry(pos, head, member)                                                     \
    for (pos = container_of((head)->next, __typeof__(*pos), member); &pos->member != (head);       \
         pos = container_of(pos->member.next, __typeof__(*pos), member))
struct kgsl_device {
    s64 total;
};
struct page {
    int value;
};
struct entry {
    struct {
        u64 size;
    } memdesc;
};
struct scatterlist {
    struct page *page;
};
struct table {
    struct scatterlist *sgl;
};
struct dmabuf_list_entry {
    struct kgsl_device *device;
    u64 size;
    struct page *firstpage;
    struct list_head node, dmabuf_list;
};
struct kgsl_dma_buf_meta {
    struct entry *entry;
    struct table *table;
    struct dmabuf_list_entry *dle;
    struct list_head node;
};
static struct list_head kgsl_dmabuf_list;
static int kgsl_dmabuf_lock, fail_alloc;
#define GFP_ATOMIC 0
#define spin_lock(x) ((void)(x))
#define spin_unlock(x) ((void)(x))
#define sg_page(sg) ((sg)->page)
static void *kzalloc(size_t size, int flags) {
    (void)flags;
    return fail_alloc ? NULL : calloc(1, size);
}
#define kfree free
static void kgsl_trace_gpu_mem_total(struct kgsl_device *d, s64 delta) {
    d->total += delta;
    assert(d->total >= 0);
}
static void add_dmabuf_list(struct kgsl_device *device, struct kgsl_dma_buf_meta *meta) {
    struct dmabuf_list_entry *dle;
    struct page *page;

    /*
     * Get the first page. We will use it to identify the imported
     * buffer, since the same buffer can be mapped as different
     * mem entries.
     */
    page = sg_page(meta->table->sgl);

    spin_lock(&kgsl_dmabuf_lock);

    /* Go through the list to see if we imported this buffer before */
    list_for_each_entry(dle, &kgsl_dmabuf_list, node) {
        if (dle->firstpage == page) {
            /* Add the dmabuf meta to the list for this dle */
            meta->dle = dle;
            list_add(&meta->node, &dle->dmabuf_list);
            spin_unlock(&kgsl_dmabuf_lock);
            return;
        }
    }

    /* This is a new buffer. Add a new entry for it */
    dle = kzalloc(sizeof(*dle), GFP_ATOMIC);
    if (dle) {
        dle->device = device;
        dle->size = meta->entry->memdesc.size;
        dle->firstpage = page;
        INIT_LIST_HEAD(&dle->dmabuf_list);
        list_add(&dle->node, &kgsl_dmabuf_list);
        meta->dle = dle;
        list_add(&meta->node, &dle->dmabuf_list);
        kgsl_trace_gpu_mem_total(device, dle->size);
    }
    spin_unlock(&kgsl_dmabuf_lock);
}

static void remove_dmabuf_list(struct kgsl_dma_buf_meta *meta) {
    struct dmabuf_list_entry *dle = meta->dle;

    if (!dle)
        return;

    spin_lock(&kgsl_dmabuf_lock);
    list_del(&meta->node);
    if (list_empty(&dle->dmabuf_list)) {
        list_del(&dle->node);
        kgsl_trace_gpu_mem_total(dle->device, -(s64)dle->size);
        kfree(dle);
    }
    spin_unlock(&kgsl_dmabuf_lock);
}

int main(void) {
    struct kgsl_device dev = {0};
    struct page page = {0};
    struct scatterlist sg = {.page = &page};
    struct table tab = {.sgl = &sg};
    struct entry e1 = {.memdesc.size = 4096}, e2 = {.memdesc.size = 4096};
    struct kgsl_dma_buf_meta a = {.entry = &e1, .table = &tab}, b = {.entry = &e2, .table = &tab};
    INIT_LIST_HEAD(&kgsl_dmabuf_list);
    add_dmabuf_list(&dev, &a);
    assert(dev.total == 4096);
    add_dmabuf_list(&dev, &b);
    assert(dev.total == 4096);
    remove_dmabuf_list(&a);
    assert(dev.total == 4096);
    remove_dmabuf_list(&b);
    assert(dev.total == 0);
    assert(list_empty(&kgsl_dmabuf_list));
    puts("PASS shared DMA-BUF counted once; either importer can release first");
    a.dle = b.dle = NULL;
    add_dmabuf_list(&dev, &a);
    add_dmabuf_list(&dev, &b);
    remove_dmabuf_list(&b);
    assert(dev.total == 4096);
    remove_dmabuf_list(&a);
    assert(dev.total == 0);
    puts("PASS reverse release order balances global counter");
    a.dle = b.dle = NULL;
    add_dmabuf_list(&dev, &a);
    add_dmabuf_list(&dev, &b);
    remove_dmabuf_list(&a);
    e2.memdesc.size = 8192;
    remove_dmabuf_list(&b);
    assert(dev.total == 0);
    puts("PASS last release deducts original recorded size");
    a.dle = NULL;
    fail_alloc = 1;
    add_dmabuf_list(&dev, &a);
    assert(dev.total == 0 && a.dle == NULL);
    remove_dmabuf_list(&a);
    assert(dev.total == 0);
    puts("PASS accounting-node allocation failure cannot underflow counter");
    return 0;
}
