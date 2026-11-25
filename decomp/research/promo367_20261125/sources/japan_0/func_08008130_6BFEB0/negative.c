#include "m2c_types.h"
extern char func_80023AB0_246B0;
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
extern M2C_UNK func_080081A8_6BFF28;

void func_08008130_6BFEB0(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        ((M2C_UNK(*)())&func_80038808_39408)(0x10A, arg0);
        ((M2C_UNK(*)())&func_80023AB0_246B0)(0);
        M2C_FIELD(arg0, u16 *, 0x8A) = 0xFU;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_080081A8_6BFF28, arg0);
    }
}
