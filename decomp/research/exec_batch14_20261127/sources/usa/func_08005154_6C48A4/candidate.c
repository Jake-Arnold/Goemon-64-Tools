#include "m2c_types.h"

extern u8 func_80024038_24C38[];
extern u8 func_8003521C_35E1C[];
extern u8 func_80038B98_39798[];
extern u8 func_080051F4_6C4944[];

void func_08005154_6C48A4(void *arg0, void *arg1) {
    u16 var_v0;

    M2C_FIELD(arg1, u16 *, 0x16) = (M2C_FIELD(arg1, u16 *, 0x16) + 0x20) & 0x3FF;
    var_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    if (var_v0 == 0x14) {
        ((void (*)(s32))func_80024038_24C38)(0x135);
        var_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    }
    M2C_FIELD(arg0, u16 *, 0x8A) = var_v0 - 1;
    if (var_v0 == 0) {
        ((void (*)(s32))func_80038B98_39798)(0x12D);
        M2C_FIELD(arg0, s32 *, 0x60) = 0x02A007E1;
        M2C_FIELD(arg0, s8 *, 0x75) = 0xA;
        ((void (*)(void *))func_8003521C_35E1C)(func_080051F4_6C4944);
    }
}
