#include "m2c_types.h"

extern u8 func_80034E8C_35A8C[];
extern u8 func_8021EFDC_5DA56C[];
extern u8 func_08004CF4_6C8EB4[];

void func_08004E60_6C9020(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, u8 *, 0xDC) -= 8;
    ((void (*)(void *, u8, s32, s32, s32))func_8021EFDC_5DA56C)(arg0, M2C_FIELD(arg0, u8 *, 0xDC), 0, 0, 0xC8);
    if (M2C_FIELD(arg0, u8 *, 0xDC) < 9) {
        M2C_FIELD(arg0, u8 *, 0xDC) = 8;
        ((void (*)(void *))func_80034E8C_35A8C)(func_08004CF4_6C8EB4);
    }
}
