#include "m2c_types.h"
s32 func_80014480_15080(s32, M2C_UNK);              /* extern */
s32 func_80034A48_35648(M2C_UNK (*)(), M2C_UNK);    /* extern */
M2C_UNK func_80038838_39438(M2C_UNK);               /* extern */
M2C_UNK func_801E9920_6143A0();                     /* static */
extern s32 D_80214640_63F0C0;
extern s32 g_system_ptr;

s32 func_801E9CE4_614764(void) {
    s32 sp18;
    s32 temp_v0;
    s32 temp_v0_2;

    D_80214640_63F0C0 = 0;
    temp_v0_2 = func_80014480_15080(g_system_ptr + 0xC7FA4, 4);
    if (temp_v0_2 == 0) {
        return 0;
    }
    D_80214640_63F0C0 = temp_v0_2;
    temp_v0 = func_80034A48_35648(func_801E9920_6143A0, 0);
    sp18 = temp_v0;
    func_80038838_39438(0x43);
    return temp_v0;
}
