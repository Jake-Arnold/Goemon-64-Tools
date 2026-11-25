#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_8003D310_3DF10;
M2C_UNK func_08002AD8_728F68();                     /* static */

void func_08002A80_728F10(void *arg0, void *arg1) {
    M2C_FIELD(arg1, u16 *, 0x16) = (u16) ((M2C_FIELD(arg1, u16 *, 0x16) + 1) & 0x3FF);
    if (M2C_FIELD(arg0, s32 *, 0x68) & 0x200) {
        ((M2C_UNK(*)())&func_8003D310_3DF10)(0x80);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08002AD8_728F68);
    }
}
