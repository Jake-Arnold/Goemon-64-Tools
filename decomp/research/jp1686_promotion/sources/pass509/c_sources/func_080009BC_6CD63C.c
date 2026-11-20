#include "m2c_types.h"
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
M2C_UNK func_08000A60_6CD6E0();                     /* static */

void func_080009BC_6CD63C(void *arg0, void *arg1) {
    if (((s32(*)())&func_80023D9C_2499C)(0x16C) == 0) {
        if (M2C_FIELD(arg1, u8 *, 0x7C) & 4) {
            M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (M2C_FIELD(arg0, u16 *, 0x8A) + 1);
        }
        if (M2C_FIELD(arg0, u16 *, 0x8A) == 2) {
            M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 0x01000000);
            ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 0, 0x3E800000, 4);
            ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08000A60_6CD6E0);
        }
    }
}
