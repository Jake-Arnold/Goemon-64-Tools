#include "m2c_types.h"
void *func_80014480_15080(s32, M2C_UNK);            /* extern */
s32 func_80034A48_35648(M2C_UNK (*)(), M2C_UNK);    /* extern */
M2C_UNK func_801E8760_6131E0();                     /* static */
extern void *D_80214630_63F0B0;
extern s32 g_system_ptr;

s32 func_801E89CC_61344C(u8 arg0) {
    s32 temp_v0;
    void *temp_v0_2;

    D_80214630_63F0B0 = NULL;
    temp_v0_2 = func_80014480_15080(g_system_ptr + 0xC7FA4, 0x10);
    D_80214630_63F0B0 = temp_v0_2;
    if (temp_v0_2 == NULL) {
        return 0;
    }
    temp_v0 = func_80034A48_35648(func_801E8760_6131E0, 0);
    M2C_FIELD(D_80214630_63F0B0, s32 *, 0) = temp_v0;
    M2C_FIELD(D_80214630_63F0B0, u8 *, 0xC) = arg0;
    M2C_FIELD(D_80214630_63F0B0, s8 *, 0xD) = 0;
    return temp_v0;
}
