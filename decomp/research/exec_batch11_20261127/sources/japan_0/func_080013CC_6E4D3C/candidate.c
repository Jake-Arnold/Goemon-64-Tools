#include "m2c_types.h"

extern u8 func_80034E8C_35A8C[];
extern f32 D_08004D50_6E86C0;
extern u8 func_0800141C_6E4D8C[];

void func_080013CC_6E4D3C(void *arg0, void *arg1) {
    f32 val;
    s32 temp_v0;

    val = D_08004D50_6E86C0;
    M2C_FIELD(arg1, f32 *, 0x1C) = val;
    M2C_FIELD(arg1, f32 *, 0x20) = val;
    M2C_FIELD(arg1, f32 *, 0x24) = val;
    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = temp_v0 - 1;
    if (temp_v0 == 0) {
        ((void (*)(void *))func_80034E8C_35A8C)(func_0800141C_6E4D8C);
    }
}
