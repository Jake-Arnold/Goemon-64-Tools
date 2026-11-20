#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
M2C_UNK func_080070E4_6CB2A4();                     /* static */

void func_08007094_6CB254(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 0xC8;
        ((M2C_UNK(*)())&func_80038808_39408)(0x8122);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080070E4_6CB2A4);
    }
}
