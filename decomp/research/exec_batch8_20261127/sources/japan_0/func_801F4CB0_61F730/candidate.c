#include "m2c_types.h"
void func_80034E8C_35A8C(void *);
void func_80038838_39438(s32);
void func_801D898C_60340C(s32, f32);
void func_801DB75C_6061DC(s32);
f32 func_801FC898_627318(void);
void func_801FCC14_627694(s32, f32, f32, f32);
extern u8 *D_80214600_63F080;
extern u8 func_801F4D60_61F7E0[];

typedef struct {
    u8 pad0[0xC];
    f32 unkC;
    u8 pad10[0x10];
    f32 unk20;
} Arg1_61A960;

void func_801F4CB0_61F730(s32 arg0, Arg1_61A960 *arg1) {
    f32 temp;

    if (M2C_FIELD(D_80214600_63F080, u8 *, 0x2C1) == 3) {
        func_801D898C_60340C(arg0, 40.0f);
        func_801DB75C_6061DC(arg0);
        temp = func_801FC898_627318() - (450.0f * arg1->unk20);
        if (temp <= arg1->unkC) {
            func_80038838_39438(0x12F);
            func_801FCC14_627694(arg0, 0.8f, 0.6f, 0.4f);
            func_80034E8C_35A8C(func_801F4D60_61F7E0);
        }
    }
}
