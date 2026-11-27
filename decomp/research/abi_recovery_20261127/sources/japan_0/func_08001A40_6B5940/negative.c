#include "m2c_types.h"
M2C_UNK func_08001A04_6B5904(void *);                     /* extern */
extern char func_80034E8C_35A8C;
extern char func_8021BB68_5D70F8;
extern char func_8021EB78_5DA108;
extern M2C_UNK func_08001AD8_6B59D8;

void func_08001A40_6B5940(void *arg0, void *arg1) {
    func_08001A04_6B5904(arg0);
    M2C_FIELD(arg0, s8 *, 0x6C) = 0;
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x2F1;
    ((M2C_UNK (*)(void *, M2C_UNK))&func_8021BB68_5D70F8)(arg0, 0);
    M2C_FIELD(arg1, f32 *, 8) = 15.0f;
    M2C_FIELD(arg1, f32 *, 0xC) = -52.0f;
    M2C_FIELD(arg1, f32 *, 0x10) = -18.0f;
    ((M2C_UNK (*)(void *, M2C_UNK))&func_8021EB78_5DA108)(arg0, 0x3F666666);
    ((M2C_UNK (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_08001AD8_6B59D8);

    *(volatile s32 *)0x80000000 = 1;
}
