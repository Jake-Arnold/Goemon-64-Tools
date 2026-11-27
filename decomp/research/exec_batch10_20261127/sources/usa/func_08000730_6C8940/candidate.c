#include "m2c_types.h"
extern M2C_UNK func_80024038_24C38;
extern M2C_UNK func_8003521C_35E1C;
extern M2C_UNK func_080007CC_6C89DC;

typedef struct {
    u8 unk_00[0x78];
    f32 unk_78;
    f32 unk_7C;
    f32 unk_80;
    u8 unk_84[0x6];
    u16 unk_8A;
} Obj0_08000730;

typedef struct {
    u8 unk_00[0x28];
    f32 unk_28;
    u8 unk_2C[0x50];
    u8 unk_7C;
    u8 unk_7D;
    s16 unk_7E;
} Obj1_08000730;

void func_08000730_6C8940(Obj0_08000730 *arg0, Obj1_08000730 *arg1) {
    if (arg1->unk_28 >= 12.0f) {
        arg0->unk_80 = 0.0f;
        arg0->unk_7C = 0.0f;
        arg0->unk_78 = 0.0f;
        arg1->unk_7E = 0x20;
    }
    if (arg1->unk_7C & 2) {
        if (arg0->unk_8A++ >= 0xF) {
            arg0->unk_8A = 0;
            ((void (*)(s32))&func_80024038_24C38)(0x16A);
            ((void (*)(void *))&func_8003521C_35E1C)(&func_080007CC_6C89DC);
        }
    }
}
