#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
f32 func_801D8660_6030E0(void *, M2C_UNK, void *, void *); /* extern */
M2C_UNK func_80204FE4_62FA64();                     /* static */
extern void *func_80214670_5CFC00;

void func_80204EC8_62F948(void *arg0, void *arg1) {
    M2C_FIELD(func_80214670_5CFC00, s8 *, 0x816) = 2;
    if (func_801D8660_6030E0(arg1, 0x41200000, arg0, arg1) == 0.0f) {
        if (M2C_FIELD(arg1, f32 *, 8) >= 0.0f) {
            M2C_FIELD(arg0, f32 *, 0x70) = -10.0f;
        } else {
            M2C_FIELD(arg0, f32 *, 0x70) = 10.0f;
        }
        if (M2C_FIELD(arg1, f32 *, 0xC) >= -80.0f) {
            M2C_FIELD(arg0, f32 *, 0x74) = -6.0f;
        } else {
            M2C_FIELD(arg0, f32 *, 0x74) = 6.0f;
        }
        if (M2C_FIELD(arg1, f32 *, 0x10) <= -300.0f) {
            M2C_FIELD(arg0, f32 *, 0x78) = -4.0f;
        } else {
            M2C_FIELD(arg0, f32 *, 0x78) = -10.0f;
        }
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x28;
        func_80034E8C_35A8C(func_80204FE4_62FA64);
    }
}
