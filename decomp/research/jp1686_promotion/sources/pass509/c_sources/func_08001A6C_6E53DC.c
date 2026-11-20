#include "m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_08001AAC_6E541C();                     /* static */

void func_08001A6C_6E53DC(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x28;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001AAC_6E541C);
    }
}
