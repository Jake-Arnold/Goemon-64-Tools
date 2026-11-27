#include "m2c_types.h"
extern M2C_UNK func_8003521C_35E1C;
extern M2C_UNK func_80038B98_39798;
extern M2C_UNK func_801DCD48_598C58;
extern M2C_UNK func_80214B4C_5D001C;

typedef struct {
    u8 unk_00[0x68];
    s32 unk_68;
} Obj_80214AEC;

void func_80214AEC_5CFFBC(Obj_80214AEC *arg0, s32 arg1) {
    if (arg0->unk_68 & 0x200) {
        ((void (*)(s32))&func_80038B98_39798)(0x26C);
        ((void (*)(s32))&func_801DCD48_598C58)(2);
        ((void (*)(void *))&func_8003521C_35E1C)(&func_80214B4C_5D001C);
    }

    *(volatile s32 *)0x80000000 = 1;
}
