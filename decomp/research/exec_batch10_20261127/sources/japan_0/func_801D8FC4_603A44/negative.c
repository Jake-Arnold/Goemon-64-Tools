#include "m2c_types.h"
typedef struct {
    u8 pad0[0x68];
    s32 unk68;
} UnkGlobal;
extern UnkGlobal *D_80214600_63F080;

s32 func_801D8FC4_603A44(s32 arg0) {
    UnkGlobal *p = D_80214600_63F080;
    p->unk68 -= arg0;
    if (p->unk68 >= 0x3E7) {
        p->unk68 = 0x3E7;
    }
    if (p->unk68 <= 0) {
        p->unk68 = 0;
    }
    { *(volatile s32 *)0x80000000 = 1; } return p->unk68;
}
