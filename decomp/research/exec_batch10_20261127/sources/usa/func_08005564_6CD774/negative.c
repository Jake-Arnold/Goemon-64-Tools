#include "m2c_types.h"
extern M2C_UNK func_80024038_24C38;
extern M2C_UNK func_8003521C_35E1C;
extern M2C_UNK func_080055C0_6CD7D0;

typedef struct {
    u8 unk_00[0x8A];
    u16 unk_8A;
} Obj_08005564;

void func_08005564_6CD774(Obj_08005564 *arg0, s32 arg1) {
    if (arg0->unk_8A++ >= 0xA) {
        arg0->unk_8A = 0;
        ((void (*)(s32))&func_80024038_24C38)(0x164);
        ((void (*)(void *))&func_8003521C_35E1C)(&func_080055C0_6CD7D0);
    }

    *(volatile s32 *)0x80000000 = 1;
}
