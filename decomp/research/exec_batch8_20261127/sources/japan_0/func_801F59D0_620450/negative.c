#include "m2c_types.h"

void func_80034E8C_35A8C(void (*)(void));
f32 func_801D8660_6030E0(s32, f32);
void func_801D88EC_60336C(s32, void *);
s32 func_801D9404_603E84(f32, f32, f32, s32, s32);
void func_801D9620_6040A0(s32, s32, s32);
void func_801FCE00_627880(s32, s32);
extern u8 D_80210990_63B410[];
void func_801F5A60_6204E0(void);

void func_801F59D0_620450(s32 arg0, s32 arg1) {
    func_801FCE00_627880(arg0, arg1);
    func_801D9620_6040A0(arg0, 0, 8);
    if ((func_801D9404_603E84(0.0f, 0.0f, 0.0f, arg0, 0xA) != 0) &&
        (func_801D8660_6030E0(arg1, 50.0f) == 0.0f)) {
        func_801D88EC_60336C(arg0, D_80210990_63B410);
        func_80034E8C_35A8C(func_801F5A60_6204E0);
    }

    *(volatile s32 *)0x80000000 = 1;
}
