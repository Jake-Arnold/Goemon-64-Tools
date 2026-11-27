#include "m2c_types.h"
void func_8003521C_35E1C(void *);
void func_80038BC8_397C8(s32);
void func_801D326C_5FE64C(s32, f32);
void func_801D603C_60141C(s32);
f32 func_801F7168_622548(void);
void func_801F74E4_6228C4(s32, f32, f32, f32);
extern u8 *D_8020EED0_63A2B0;
extern u8 func_801EF630_61AA10[];

typedef struct {
    u8 pad0[0xC];
    f32 unkC;
    u8 pad10[0x10];
    f32 unk20;
} Arg1_61A960;

void func_801EF580_61A960(s32 arg0, Arg1_61A960 *arg1) {
    f32 temp;

    if (M2C_FIELD(D_8020EED0_63A2B0, u8 *, 0x2C1) == 3) {
        func_801D326C_5FE64C(arg0, 40.0f);
        func_801D603C_60141C(arg0);
        temp = func_801F7168_622548() - (450.0f * arg1->unk20);
        if (temp <= arg1->unkC) {
            func_80038BC8_397C8(0x12F);
            func_801F74E4_6228C4(arg0, 0.8f, 0.6f, 0.4f);
            func_8003521C_35E1C(func_801EF630_61AA10);
        }
    }
}
