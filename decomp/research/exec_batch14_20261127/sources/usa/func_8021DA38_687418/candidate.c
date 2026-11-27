#include "m2c_types.h"

s32 func_8000DBF0_E7F0(s32, s32, s32, s32, f32, f32, s32, s32, s32, f32, f32, f32, s32, s32);
s32 func_80034E08_35A08(s32, void *, s32);
extern u8 D_8022A270_693C50[];
extern f32 D_8022AD28_694708;
extern u8 func_08001F90_6B13A0[];
extern u8 func_8021D5DC_686FBC[];

s32 func_8021DA38_687418(s32 arg0, s32 arg1, f32 arg2, f32 arg3) {
    s32 sp44;
    void *temp_v1;
    f32 temp_f0;

    sp44 = func_80034E08_35A08(arg0, func_8021D5DC_686FBC, 0);
    if (sp44 == 0) {
        return 0;
    }
    temp_f0 = D_8022AD28_694708;
    temp_v1 = (void *)(sp44 + 0x5C);
    M2C_FIELD(temp_v1, s32 *, 0x2C) = func_8000DBF0_E7F0(
        sp44,
        (s32)func_08001F90_6B13A0 + 0x10000000,
        (s32)D_8022A270_693C50 | 0x10000000,
        arg1,
        arg2,
        arg3,
        0,
        0,
        0,
        temp_f0,
        temp_f0,
        temp_f0,
        0x4E1,
        0
    );
    M2C_FIELD(temp_v1, f32 *, 0xC) = 255.0f;
    return sp44;
}
