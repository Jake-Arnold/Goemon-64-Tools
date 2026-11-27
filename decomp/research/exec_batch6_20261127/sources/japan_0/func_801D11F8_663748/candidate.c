#include "m2c_types.h"
s32 func_8001019C_10D9C(void *, s32, s32);
void func_80011184_11D84(void *, s32, s32);
void func_80011560_12160(void *, s32);
void *func_80034A78_35678(u8 *, void *, s32);
extern M2C_UNK func_801D0E84_6633D4;
extern M2C_UNK func_801D11D8_663728;

void *func_801D11F8_663748(u8 *arg0, s32 arg1, s32 arg2, s32 arg3) {
    s32 temp_v0_2;
    void *temp_v0;

    temp_v0 = func_80034A78_35678(arg0, &func_801D0E84_6633D4, 0);
    if (temp_v0 == NULL) {
        return NULL;
    }
    M2C_FIELD(temp_v0, u8 **, 0x5C) = arg0 + 0x5C;
    M2C_FIELD(temp_v0, M2C_UNK **, 0x60) = &func_801D11D8_663728;
    func_80011184_11D84(temp_v0, arg1, arg2);
    temp_v0_2 = func_8001019C_10D9C(temp_v0, 0x14, arg3);
    M2C_FIELD(temp_v0, s32 *, 0x78) = temp_v0_2;
    if (temp_v0_2 == -1) {
        return NULL;
    }
    func_80011560_12160(temp_v0, arg3);
    return temp_v0;
}
