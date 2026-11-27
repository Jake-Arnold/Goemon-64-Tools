#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_80216DF8_5D22C8(void *, M2C_UNK);      /* extern */
M2C_UNK func_80219E08_5D52D8(void *, M2C_UNK);      /* extern */
s32 func_8021A26C_5D573C(void *, M2C_UNK, M2C_UNK, M2C_UNK, s32); /* extern */
M2C_UNK func_8021A310_5D57E0(void *);               /* extern */
M2C_UNK func_80224ABC_5DFF8C(void *, M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
extern M2C_UNK func_80213A9C_5CEF6C;

void func_802139E0_5CEEB0(void *arg0, void *arg1) {
    M2C_FIELD(arg1, s32 *, 0x30) = (s32) (func_8021A26C_5D573C(arg0, 0x8C, 0xFF, 0xFF, 0) | 0x40000000 | 0x20000000);
    M2C_FIELD(arg0, s16 *, 0x5E) = 1;
    M2C_FIELD(arg0, s32 *, 0x60) = 0x22A;
    func_80216DF8_5D22C8(arg0, 5);
    func_8021A310_5D57E0(arg0);
    func_80219E08_5D52D8(arg0, 0x3F4CCCCD);
    func_80224ABC_5DFF8C(arg0, 1, 0x3F000000, 1);
    M2C_FIELD(arg0, s8 *, 0xD5) = 1;
    M2C_FIELD(arg0, s32 *, 0x64) = (s32) (M2C_FIELD(arg0, s32 *, 0x64) | 2);
    func_8003521C_35E1C(&func_80213A9C_5CEF6C);

    *(volatile int *)0x80000000 = 1;
}
