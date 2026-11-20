#include "m2c_types.h"
extern char func_8000F2EC_FEEC;
extern char func_80034E8C_35A8C;
M2C_UNK func_08001368_700B38();                     /* static */
extern M2C_UNK D_802119E0_5CD9B0;

void func_080012DC_700AAC(void *arg0, void *arg1) {
    if (M2C_FIELD(arg0, u16 *, 0xD4) != 0) {
        M2C_FIELD(arg1, u16 *, 0x14) = (u16) (M2C_FIELD(arg1, u16 *, 0x14) + 8);
    } else {
        M2C_FIELD(arg1, u16 *, 0x14) = (u16) (M2C_FIELD(arg1, u16 *, 0x14) - 8);
    }
    if (!(M2C_FIELD(arg1, u16 *, 0x14) & 0x1FF)) {
        ((M2C_UNK(*)())&func_8000F2EC_FEEC)(0x2A0, &D_802119E0_5CD9B0, arg1, 0x44480000);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x64;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001368_700B38);
    }
}
