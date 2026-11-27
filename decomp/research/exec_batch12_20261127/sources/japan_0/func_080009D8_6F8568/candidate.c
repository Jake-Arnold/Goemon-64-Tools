#include "m2c_types.h"

extern u8 func_80034E8C_35A8C[];
extern u8 func_8021EFDC_5DA56C[];
extern u8 func_08000A60_6F85F0[];

void func_080009D8_6F8568(void *arg0, void *arg1) {
    M2C_FIELD(arg1, u16 *, 0x16) = (u16) ((M2C_FIELD(arg1, u16 *, 0x16) + 0x40) & 0x3FF);
    M2C_FIELD(arg0, u8 *, 0xD1) = (u8) (M2C_FIELD(arg0, u8 *, 0xD1) - 2);
    ((void (*)(void *, u8, s32, s32, s32))func_8021EFDC_5DA56C)(arg0, M2C_FIELD(arg0, u8 *, 0xD1), 0, 0, 0);
    if (M2C_FIELD(arg0, u8 *, 0xD1) == 0) {
        ((void (*)(u8 *))func_80034E8C_35A8C)(func_08000A60_6F85F0);
        M2C_FIELD(arg0, s16 *, 0x8A) = 5;
        M2C_FIELD(arg0, s32 *, 0x60) = 0;
    }
}
