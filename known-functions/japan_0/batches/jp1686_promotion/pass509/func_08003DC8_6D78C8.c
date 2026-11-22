#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
extern char func_8021F3B4_5DA944;
extern char func_8022982C_5E4DBC;
M2C_UNK func_08003EC0_6D79C0();                     /* static */
M2C_UNK func_08004028_6D7B28();                     /* static */

void func_08003DC8_6D78C8(s32 arg0, M2C_UNK arg1) {
    s32 temp_v0;

    ((M2C_UNK(*)())&func_8021F3B4_5DA944)();
    ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 0, 0x3F800000, 0);
    M2C_FIELD(arg0, s16 *, 0x8A) = (s16) (((u32) ((arg0 & 0x3FF) * 0x12C) >> 0xA) + 2);
    ((M2C_UNK(*)())&func_8022982C_5E4DBC)(arg0, 0, 0x3F800000, 0);
    temp_v0 = M2C_FIELD(arg0, s32 *, 0xD0);
    switch (temp_v0) {                              /* irregular */
    case 0:
        M2C_FIELD(arg0, s32 *, 0x60) = 0x2A0CE3;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08003EC0_6D79C0);
        return;
    case 1:
        M2C_FIELD(arg0, s32 *, 0x60) = 0x2A0EE3;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08004028_6D7B28);
        return;
    }
}
