#include "m2c_types.h"
s32 func_080016A8_6D51A8();                         /* extern */
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
extern char func_8021E46C_5D99FC;
extern M2C_UNK func_08001D7C_6D587C;

void func_08001CD0_6D57D0(void *arg0, M2C_UNK arg1) {
    if (func_080016A8_6D51A8() == 0) {
        M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
        if (((s32  (*)(void *, f32, f32, f32, s32))&func_8021E46C_5D99FC)(arg0, (f32) M2C_FIELD(arg0, s16 *, 0xA0), 0.0f, (f32) M2C_FIELD(arg0, s16 *, 0xA2), 8) == 0) {
            ((M2C_UNK  (*)(void *, u8, f32, M2C_UNK))&func_8021B3BC_5D694C)(arg0, M2C_FIELD(arg0, u8 *, 0xA8), 0.25f, 1);
            ((M2C_UNK (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_08001D7C_6D587C);
        }
    }

    *(volatile s32 *)0x80000000 = 1;
}
