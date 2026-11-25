#include "m2c_types.h"
extern char func_8000F198_FD98;
extern char func_80034E8C_35A8C;
extern char func_8021BB68_5D70F8;
extern char func_8021F080_5DA610;
extern char func_8022982C_5E4DBC;
extern M2C_UNK D_802119E0_5CD9B0;
extern M2C_UNK func_08003424_6B7324;

void func_08003364_6B7264(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        ((M2C_UNK(*)())&func_8000F198_FD98)(0x105, &D_802119E0_5CD9B0, arg1, 0x43C80000);
        M2C_FIELD(arg0, s16 *, 0x5E) = 0x7E;
        M2C_FIELD(arg0, s32 *, 0x60) = 0x222;
        M2C_FIELD(arg0, u8 *, 0xD0) = 0xFC;
        ((M2C_UNK(*)())&func_8021BB68_5D70F8)(arg0, 3);
        ((M2C_UNK(*)())&func_8021F080_5DA610)(arg0);
        ((M2C_UNK(*)())&func_8022982C_5E4DBC)(arg0, 0, 0x3FC00000, 0);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_08003424_6B7324);
    }
}
