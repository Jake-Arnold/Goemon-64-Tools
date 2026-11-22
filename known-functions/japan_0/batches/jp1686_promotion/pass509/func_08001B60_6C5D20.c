#include "m2c_types.h"
extern char func_8000F1E0_FDE0;
extern char func_80034E8C_35A8C;
M2C_UNK func_08001BBC_6C5D7C();                     /* static */
extern M2C_UNK D_802119E0_5CD9B0;

void func_08001B60_6C5D20(void *arg0, M2C_UNK arg1) {
    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        ((M2C_UNK(*)())&func_8000F1E0_FDE0)(0x272, &D_802119E0_5CD9B0, arg1, 0x461C4000);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001BBC_6C5D7C);
    }
}
