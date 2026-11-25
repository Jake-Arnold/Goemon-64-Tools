#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern M2C_UNK func_08002CC8_6BAA48;

void func_08002C74_6BA9F4(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_v0;

    M2C_FIELD(arg1, u16 *, 0x16) = (u16) ((M2C_FIELD(arg1, u16 *, 0x16) - 1) & 0x3FF);
    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        M2C_FIELD(arg0, u16 *, 0x8A) = 0xAU;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_08002CC8_6BAA48);
    }
}
