#include "m2c_types.h"
typedef struct {
    u8 pad0[0x64];
    s32 unk64;
} UnkGlobal;
extern UnkGlobal *D_8020EED0_63A2B0;

s32 func_801D3A68_5FEE48(s32 arg0) {
    UnkGlobal *p = D_8020EED0_63A2B0;
    p->unk64 += arg0;
    if (p->unk64 <= 0) {
        p->unk64 = 0;
    }
    if (p->unk64 >= 0x3E7) {
        p->unk64 = 0x3E7;
    }
    return p->unk64;
}
