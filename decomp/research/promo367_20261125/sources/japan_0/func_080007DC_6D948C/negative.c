#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
extern M2C_UNK func_08000880_6D9530;

void func_080007DC_6D948C(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        if (M2C_FIELD(arg0, u16 *, 0xD4) & 2) {
            M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 0x01000000);
        } else {
            M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & 0xFEFFFFFF);
        }
        ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, M2C_FIELD(arg0, u16 *, 0xD2), 0x3F000000, 0);
        M2C_FIELD(arg0, s16 *, 0xD8) = 0;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_08000880_6D9530);
    }
}
