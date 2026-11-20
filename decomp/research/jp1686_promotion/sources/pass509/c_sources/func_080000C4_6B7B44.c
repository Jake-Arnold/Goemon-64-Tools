#include "m2c_types.h"
extern char func_8000F1E0_FDE0;
extern char func_80034E8C_35A8C;
M2C_UNK func_0800011C_6B7B9C();                     /* static */
extern M2C_UNK D_802119E0_5CD9B0;

void func_080000C4_6B7B44(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, s32 *, 0x68) & 1) {
        ((M2C_UNK(*)())&func_8000F1E0_FDE0)(0x26E, &D_802119E0_5CD9B0, arg1, 0x44480000);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_0800011C_6B7B9C);
    }
}
