#include "m2c_types.h"
extern M2C_UNK func_80023CF8_248F8;
extern M2C_UNK func_80034E8C_35A8C;
extern M2C_UNK func_08005574_6D21F4;

typedef struct {
    u8 unk_00[0x8A];
    u16 unk_8A;
} Obj_08005564;

void func_08005518_6D2198(Obj_08005564 *arg0, s32 arg1) {
    if (arg0->unk_8A++ >= 0xA) {
        arg0->unk_8A = 0;
        ((void (*)(s32))&func_80023CF8_248F8)(0x164);
        ((void (*)(void *))&func_80034E8C_35A8C)(&func_08005574_6D21F4);
    }
}
