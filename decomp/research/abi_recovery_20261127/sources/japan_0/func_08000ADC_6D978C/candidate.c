#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
extern char func_8021DB3C_5D90CC;
extern char func_802213C4_5DC954;
extern M2C_UNK func_08000880_6D9530;

void func_08000ADC_6D978C(void *arg0, void *arg1) {
    M2C_FIELD(arg0, s32 *, 0x60) = 0x2E1;
    ((M2C_UNK (*)())&func_802213C4_5DC954)();
    ((M2C_UNK  (*)(void *, u16, f32, M2C_UNK))&func_8021B3BC_5D694C)(arg0, M2C_FIELD(arg0, u16 *, 0xD2), 0.0f, 0);
    if (M2C_FIELD(arg0, s32 *, 0x68) != 0) {
        M2C_FIELD(arg0, s16 *, 0xD0) = 0x14;
        M2C_FIELD(arg0, s16 *, 0xD6) = 0x28;
        M2C_FIELD(arg0, u16 *, 0xD2) = 1U;
        ((M2C_UNK (*)(void *, M2C_UNK))&func_8021DB3C_5D90CC)(arg0, 3);
    } else {
        M2C_FIELD(arg0, s16 *, 0xD0) = 0xA;
        M2C_FIELD(arg0, u16 *, 0xD2) = 0U;
        M2C_FIELD(arg0, s16 *, 0xD6) = 0x3C;
        ((M2C_UNK (*)(void *, M2C_UNK))&func_8021DB3C_5D90CC)(arg0, 2);
    }
    M2C_FIELD(arg1, u8 *, 0x7C) = (u8) (M2C_FIELD(arg1, u8 *, 0x7C) | 2);
    M2C_FIELD(arg0, s16 *, 0xD4) = 0;
    ((M2C_UNK (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_08000880_6D9530);
}
