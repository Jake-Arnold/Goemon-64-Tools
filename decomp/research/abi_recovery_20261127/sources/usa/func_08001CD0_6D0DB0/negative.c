#include "m2c_types.h"
s32 func_080016A8_6D0788();                         /* extern */
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_802196FC_5D4BCC;
extern M2C_UNK func_08001D7C_6D0E5C;

void func_08001CD0_6D0DB0(void *arg0, M2C_UNK arg1) {
    if (func_080016A8_6D0788() == 0) {
        M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
        if (((s32  (*)(void *, f32, f32, f32, s32))&func_802196FC_5D4BCC)(arg0, (f32) M2C_FIELD(arg0, s16 *, 0xA0), 0.0f, (f32) M2C_FIELD(arg0, s16 *, 0xA2), 8) == 0) {
            ((M2C_UNK  (*)(void *, u8, f32, M2C_UNK))&func_8021664C_5D1B1C)(arg0, M2C_FIELD(arg0, u8 *, 0xA8), 0.25f, 1);
            ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08001D7C_6D0E5C);
        }
    }

    *(volatile s32 *)0x80000000 = 1;
}
