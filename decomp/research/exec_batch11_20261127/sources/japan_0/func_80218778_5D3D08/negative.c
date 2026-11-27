#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
M2C_UNK func_8021BB68_5D70F8(void *, M2C_UNK);      /* extern */
M2C_UNK func_8021EB78_5DA108(void *, M2C_UNK);      /* extern */
s32 func_8021EFDC_5DA56C(void *, M2C_UNK, M2C_UNK, M2C_UNK, s32); /* extern */
M2C_UNK func_8021F080_5DA610(void *);               /* extern */
M2C_UNK func_8022982C_5E4DBC(void *, M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
extern M2C_UNK func_80218834_5D3DC4;

void func_80218778_5D3D08(void *arg0, void *arg1) {
    M2C_FIELD(arg1, s32 *, 0x30) = (s32) (func_8021EFDC_5DA56C(arg0, 0x8C, 0xFF, 0xFF, 0) | 0x40000000 | 0x20000000);
    M2C_FIELD(arg0, s16 *, 0x5E) = 1;
    M2C_FIELD(arg0, s32 *, 0x60) = 0x22A;
    func_8021BB68_5D70F8(arg0, 5);
    func_8021F080_5DA610(arg0);
    func_8021EB78_5DA108(arg0, 0x3F4CCCCD);
    func_8022982C_5E4DBC(arg0, 1, 0x3F000000, 1);
    M2C_FIELD(arg0, s8 *, 0xD5) = 1;
    M2C_FIELD(arg0, s32 *, 0x64) = (s32) (M2C_FIELD(arg0, s32 *, 0x64) | 2);
    func_80034E8C_35A8C(&func_80218834_5D3DC4);

    *(volatile int *)0x80000000 = 1;
}
