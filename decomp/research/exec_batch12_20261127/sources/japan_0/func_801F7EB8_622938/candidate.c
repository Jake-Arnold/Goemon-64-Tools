#include "m2c_types.h"

void func_80034E8C_35A8C(void *);
f32 func_801D8738_6031B8(M2C_UNK, f32);
void func_801DB350_605DD0(void *, s32, f32, u16, s32);
s32 func_801DB4B8_605F38(void *, s32, f32, f32);
void func_801DBC7C_6066FC(void *, f32, f32, f32, f32);
void func_801FD200_627C80(void *);
extern void func_801F7F84_622A04(void);

void func_801F7EB8_622938(void *arg0, M2C_UNK arg1) {
    if (func_801D8738_6031B8(arg1, 40.0f) == 0.0f) {
        func_801FD200_627C80(arg0);
    }
    func_801DBC7C_6066FC(arg0, -300.0f, 300.0f, 0.1f, 4.0f);
    M2C_FIELD(arg0, f32 *, 0x74) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    func_801DB350_605DD0(arg0, M2C_FIELD(arg0, s32 *, 0x70), M2C_FIELD(arg0, f32 *, 0x78), func_801DB4B8_605F38(arg0, 0x30, 4.0f, 3.0f), 0);
    if (--M2C_FIELD(arg0, s32 *, 0x7C) == 0) {
        func_80034E8C_35A8C(func_801F7F84_622A04);
    }
}
