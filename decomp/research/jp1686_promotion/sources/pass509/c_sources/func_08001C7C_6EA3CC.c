#include "m2c_types.h"
extern char func_8000F1E0_FDE0;
extern char func_80034E8C_35A8C;
extern char func_8021E548_5D9AD8;
M2C_UNK func_08001CE0_6EA430();                     /* static */
extern M2C_UNK D_802119E0_5CD9B0;

void func_08001C7C_6EA3CC(M2C_UNK arg0, s32 arg1) {
    if (((s32(*)())&func_8021E548_5D9AD8)(arg0, 6) == 0) {
        ((M2C_UNK(*)())&func_8000F1E0_FDE0)(0x261, &D_802119E0_5CD9B0, arg1, 0x43C80000);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001CE0_6EA430);
    }
}
