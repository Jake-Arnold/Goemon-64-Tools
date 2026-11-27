#include "m2c_types.h"
void func_80034E8C_35A8C(void *);
extern M2C_UNK func_08005CB0_6C9E70;

void func_08005C3C_6C9DFC(void *arg0, void *arg1) {
    void (*fn)(void *) = func_80034E8C_35A8C;
    f32 temp_f0;

    temp_f0 = (f32) M2C_FIELD(arg0, s16 *, 0xA0);
    if (!(M2C_FIELD(arg1, f32 *, 0xC) < temp_f0)) {
        M2C_FIELD(arg1, f32 *, 0xC) = temp_f0;
        M2C_FIELD(arg0, u16 *, 0x8A) = M2C_FIELD(arg0, u8 *, 0xD1);
        M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
        if (M2C_FIELD(arg0, u16 *, 0x8A) == 0) {
            M2C_FIELD(arg0, u16 *, 0x8A) = 1;
        }
        fn(&func_08005CB0_6C9E70);
    }
}
