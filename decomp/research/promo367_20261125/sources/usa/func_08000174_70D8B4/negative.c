#include "m2c_types.h"
extern char func_80023DF0_249F0;
extern char func_80023E94_24A94;
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_80220F70_5DC440;
extern char func_8022125C_5DC72C;
extern char func_80224D50_5E0220;
extern char func_80226840_5E1D10;
M2C_UNK func_08000088_70D7C8();                     /* static */

void func_08000174_70D8B4(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_v1;
    s32 temp_v1_2;

    if (((s32(*)())&func_800240DC_24CDC)(0) != 0) {
        ((M2C_UNK(*)())&func_8022125C_5DC72C)(arg0);
        temp_v1 = M2C_FIELD(arg0, s32 *, 0x68);
        if (temp_v1 & 0x4000) {
            M2C_FIELD(arg0, s32 *, 0x68) = (s32) (temp_v1 & ~0x4000);
            ((M2C_UNK(*)())&func_80023DF0_249F0)(0);
            ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 1, 0x3E800000, 1);
        }
        if (((s32(*)())&func_80023E94_24A94)(0) != 0) {
            M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & 0xEFFFFFFF);
            if (M2C_FIELD(arg0, u16 *, 0xD8) != 0) {
                ((M2C_UNK(*)())&func_80226840_5E1D10)(arg0, 0x43);
            } else {
                ((M2C_UNK(*)())&func_80226840_5E1D10)(arg0, 0x44);
            }
            ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08000088_70D7C8);
            return;
        }
        goto block_10;
    }
    ((M2C_UNK(*)())&func_80220F70_5DC440)(arg0);
    temp_v1_2 = M2C_FIELD(arg0, s32 *, 0x68);
    if (temp_v1_2 & 0x4000) {
        M2C_FIELD(arg0, s32 *, 0x68) = (s32) (temp_v1_2 & ~0x4000);
        ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 1, 0x3E800000, 1);
    }
block_10:
    ((M2C_UNK(*)())&func_80224D50_5E0220)(arg0, 1);
}
