#include "m2c_types.h"
extern char func_80023AB0_246B0;
extern char func_80023B54_24754;
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
extern char func_80225CE0_5E1270;
extern char func_80225FCC_5E155C;
extern char func_80229AC0_5E5050;
extern char func_8022B5B0_5E6B40;
M2C_UNK func_08000088_711CF8();                     /* static */

void func_08000174_711DE4(void *arg0, M2C_UNK arg1) {
    s32 temp_v1;
    s32 temp_v1_2;

    if (((s32(*)())&func_80023D9C_2499C)(0) != 0) {
        ((M2C_UNK(*)())&func_80225FCC_5E155C)(arg0);
        temp_v1 = M2C_FIELD(arg0, s32 *, 0x68);
        if (temp_v1 & 0x4000) {
            M2C_FIELD(arg0, s32 *, 0x68) = (s32) (temp_v1 & ~0x4000);
            ((M2C_UNK(*)())&func_80023AB0_246B0)(0);
            ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 1, 0x3E800000, 1);
        }
        if (((s32(*)())&func_80023B54_24754)(0) != 0) {
            M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & 0xEFFFFFFF);
            if (M2C_FIELD(arg0, u16 *, 0xD8) != 0) {
                ((M2C_UNK(*)())&func_8022B5B0_5E6B40)(arg0, 0x43);
            } else {
                ((M2C_UNK(*)())&func_8022B5B0_5E6B40)(arg0, 0x44);
            }
            ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08000088_711CF8);
            return;
        }
        goto block_10;
    }
    ((M2C_UNK(*)())&func_80225CE0_5E1270)(arg0);
    temp_v1_2 = M2C_FIELD(arg0, s32 *, 0x68);
    if (temp_v1_2 & 0x4000) {
        M2C_FIELD(arg0, s32 *, 0x68) = (s32) (temp_v1_2 & ~0x4000);
        ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 1, 0x3E800000, 1);
    }
block_10:
    ((M2C_UNK(*)())&func_80229AC0_5E5050)(arg0, 1);
}
