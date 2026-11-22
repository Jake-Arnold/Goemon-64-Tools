#include "../m2c_types.h"
extern char func_8000F1E0_FDE0;
extern char func_80034E8C_35A8C;
M2C_UNK func_080022E8_701AB8();                     /* static */
extern M2C_UNK D_802119E0_5CD9B0;

void func_08002298_701A68(s32 arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_8000F1E0_FDE0)(0x155, &D_802119E0_5CD9B0, arg1, 0x43C80000);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080022E8_701AB8);
}
