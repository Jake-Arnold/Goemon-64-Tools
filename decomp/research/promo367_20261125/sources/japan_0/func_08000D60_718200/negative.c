#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80038838_39438;
extern M2C_UNK func_08000DC4_718264;

void func_08000D60_718200(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        ((M2C_UNK(*)())&func_80038838_39438)(M2C_FIELD(arg0, u16 *, 0xD8), arg0);
        M2C_FIELD(arg0, u16 *, 0x8A) = 0U;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_08000DC4_718264, arg0);
    }
}
