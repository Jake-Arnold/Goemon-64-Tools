#include "m2c_types.h"
void func_8003521C_35E1C(void *);
extern M2C_UNK func_08005CA8_6C53F8;

void func_08005C34_6C5384(void *arg0, void *arg1) {
    void (*fn)(void *) = func_8003521C_35E1C;
    f32 temp_f0;

    temp_f0 = (f32) M2C_FIELD(arg0, s16 *, 0xA0);
    if (!(M2C_FIELD(arg1, f32 *, 0xC) < temp_f0)) {
        M2C_FIELD(arg1, f32 *, 0xC) = temp_f0;
        M2C_FIELD(arg0, u16 *, 0x8A) = M2C_FIELD(arg0, u8 *, 0xD1);
        M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
        if (M2C_FIELD(arg0, u16 *, 0x8A) == 0) {
            M2C_FIELD(arg0, u16 *, 0x8A) = 1;
        }
        fn(&func_08005CA8_6C53F8);
    }

    *(volatile s32 *)0x80000000 = 1;
}
