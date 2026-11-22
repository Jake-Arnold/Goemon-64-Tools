#include "m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_08001268_6C5428();                     /* static */

void func_08001228_6C53E8(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x3C;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001268_6C5428);
    }
}
