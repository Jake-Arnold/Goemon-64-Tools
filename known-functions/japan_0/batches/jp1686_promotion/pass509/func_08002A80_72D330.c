#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8003CF80_3DB80;
M2C_UNK func_08002AD8_72D388();                     /* static */

void func_08002A80_72D330(void *arg0, void *arg1) {
    M2C_FIELD(arg1, u16 *, 0x16) = (u16) ((M2C_FIELD(arg1, u16 *, 0x16) + 1) & 0x3FF);
    if (M2C_FIELD(arg0, s32 *, 0x68) & 0x200) {
        ((M2C_UNK(*)())&func_8003CF80_3DB80)(0x80);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08002AD8_72D388);
    }
}
