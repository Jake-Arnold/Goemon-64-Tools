#include "m2c_types.h"
typedef struct {
    u8 pad0[0x68];
    s32 unk68;
} UnkGlobal;
extern UnkGlobal *D_80214600_63F080;

s32 func_801D9100_603B80(void) {
    UnkGlobal *p = D_80214600_63F080;
    if (p->unk68 >= 0x3E7) {
        p->unk68 = 0x3E7;
    }
    if (p->unk68 <= 0) {
        p->unk68 = 0;
    }
    return p->unk68;
}
