#include "m2c_types.h"
extern char func_8000FF6C_10B6C;
extern char func_800136A4_142A4;
extern char func_800143D0_14FD0;
extern char func_80034A78_35678;
M2C_UNK func_08000000_721C90();                     /* static */
M2C_UNK func_08001CD8_723968();                     /* static */
extern s32 D_08003050_724CE0;

s32 func_08002664_7242F4(s32 arg0) {
    s32 temp_v0;

    ((M2C_UNK(*)())&func_8000FF6C_10B6C)();
    ((M2C_UNK(*)())&func_800136A4_142A4)(0x4E5);
    D_08003050_724CE0 = ((s32(*)())&func_800143D0_14FD0)(func_08000000_721C90, 0x4E5);
    temp_v0 = ((s32(*)())&func_80034A78_35678)(arg0, func_08001CD8_723968, 0x3C);
    if (temp_v0 == 0) {
        return 0;
    }
    return temp_v0;
}
