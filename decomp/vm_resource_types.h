#ifndef GOEMON_VM_RESOURCE_TYPES_H
#define GOEMON_VM_RESOURCE_TYPES_H
#include "common.h"

/*
 * Only the word/halfword accesses and +4/+8 resource-context fields are typed.
 * On the big-endian N64, the numeric low halfword is at record offset +2.
 * The host test uses the numeric word because a little-endian union reverses
 * the numeric meaning of the two in-memory halfwords.
 */
typedef union {
    u32 word;
    struct {
        u16 high_half;
        u16 low_half;
    } n64_be;
} VmResourceId;

typedef struct {
    VmResourceId current_id; /* +0: word store; low numeric half at +2 on N64 */
    s32 unknown_04;          /* +4: word written from func_80001E50's result */
    s32 unknown_08;          /* +8: DDC4(start, entry ID) result minus start */
} VmResourceContext;

#ifdef GOEMON_DECOMP_HOST_TEST
#define VM_RESOURCE_ID_LOW_HALF(id_value) ((u16)((id_value).word))
#else
#define VM_RESOURCE_ID_LOW_HALF(id_value) ((id_value).n64_be.low_half)
#endif

#endif
