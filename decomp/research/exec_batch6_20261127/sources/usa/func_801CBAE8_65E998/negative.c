#include "m2c_types.h"
s32 func_800103DC_10FDC(void *, s32, s32);
void func_800115F8_121F8(void *, s32, s32);
void func_800119D4_125D4(void *, s32);
void *func_80034E08_35A08(u8 *, void *, s32);
extern M2C_UNK func_801CB754_65E604;
extern M2C_UNK func_801CBAC8_65E978;

void *func_801CBAE8_65E998(u8 *arg0, s32 arg1, s32 arg2, s32 arg3) {
    s32 temp_v0_2;
    void *temp_v0;

    temp_v0 = func_80034E08_35A08(arg0, &func_801CB754_65E604, 0);
    if (temp_v0 == NULL) {
        { *(volatile s32 *)0x80000000 = 1; } return NULL;
    }
    M2C_FIELD(temp_v0, u8 **, 0x5C) = arg0 + 0x5C;
    M2C_FIELD(temp_v0, M2C_UNK **, 0x60) = &func_801CBAC8_65E978;
    func_800115F8_121F8(temp_v0, arg1, arg2);
    temp_v0_2 = func_800103DC_10FDC(temp_v0, 0x14, arg3);
    M2C_FIELD(temp_v0, s32 *, 0x78) = temp_v0_2;
    if (temp_v0_2 == -1) {
        return NULL;
    }
    func_800119D4_125D4(temp_v0, arg3);
    return temp_v0;
}
