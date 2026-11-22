#include "m2c_types.h"
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
extern char func_801FF30C_5BB2DC;
extern char func_8021BB68_5D70F8;
M2C_UNK func_08002218_6C63D8();                     /* static */
M2C_UNK func_08002484_6C6644();                     /* static */

void func_0800211C_6C62DC(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80023D9C_2499C)(0x15A) != 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = 0x802006E1;
        ((M2C_UNK(*)())&func_8021BB68_5D70F8)(arg0, 1);
        ((M2C_UNK(*)())&func_801FF30C_5BB2DC)(0xFF, 0xFF, 0xFF);
        M2C_FIELD(arg0, s8 *, 0x6C) = 0;
        M2C_FIELD(arg0, s8 *, 0x4C) = 0;
        ((M2C_UNK(*)())&func_80038808_39408)(0x2AD);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08002484_6C6644);
        return;
    }
    M2C_FIELD(arg0, s32 *, 0x60) = 0x802006E1;
    ((M2C_UNK(*)())&func_8021BB68_5D70F8)(arg0, 0);
    ((M2C_UNK(*)())&func_801FF30C_5BB2DC)(0x78, 0x78, 0xFF);
    M2C_FIELD(arg0, s8 *, 0x6C) = 0;
    M2C_FIELD(arg0, s8 *, 0x4C) = 0;
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08002218_6C63D8);
}
