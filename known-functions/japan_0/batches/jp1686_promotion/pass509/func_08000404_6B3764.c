#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
extern char func_801E2188_59E158;
M2C_UNK func_0800047C_6B37DC();                     /* static */

void func_08000404_6B3764(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, s32 *, 0x68) & 0x200) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & 0xF7FFFFFF);
        ((M2C_UNK(*)())&func_80038808_39408)(0x26C);
        ((M2C_UNK(*)())&func_801E2188_59E158)(0x28);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_0800047C_6B37DC);
    }
}
