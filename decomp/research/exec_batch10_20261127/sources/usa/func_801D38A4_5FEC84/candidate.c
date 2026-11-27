#include "m2c_types.h"
typedef struct {
    u8 pad0[0x68];
    s32 unk68;
} UnkGlobal;
extern UnkGlobal *D_8020EED0_63A2B0;

s32 func_801D38A4_5FEC84(s32 arg0) {
    UnkGlobal *p = D_8020EED0_63A2B0;
    p->unk68 -= arg0;
    if (p->unk68 >= 0x3E7) {
        p->unk68 = 0x3E7;
    }
    if (p->unk68 <= 0) {
        p->unk68 = 0;
    }
    return p->unk68;
}
