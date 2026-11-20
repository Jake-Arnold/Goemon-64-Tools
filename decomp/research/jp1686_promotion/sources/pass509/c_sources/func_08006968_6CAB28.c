#include "m2c_types.h"
extern char func_8000F1E0_FDE0;
extern char func_80034E8C_35A8C;
M2C_UNK func_080069C8_6CAB88();                     /* static */
extern void *D_80201514_5BD4E4;
extern M2C_UNK D_802119E0_5CD9B0;

void func_08006968_6CAB28(s32 arg0, s32 arg1) {
    if (arg1 == M2C_FIELD(D_80201514_5BD4E4, s32 *, 0xA0)) {
        ((M2C_UNK(*)())&func_8000F1E0_FDE0)(0x2BA, &D_802119E0_5CD9B0, arg1, 0x43C80000);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080069C8_6CAB88);
    }
}
