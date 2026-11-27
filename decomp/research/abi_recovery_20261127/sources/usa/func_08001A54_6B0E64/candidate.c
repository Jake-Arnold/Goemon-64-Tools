#include "m2c_types.h"
M2C_UNK func_08001A18_6B0E28(void *);                     /* extern */
extern char func_8003521C_35E1C;
extern char func_80216DF8_5D22C8;
extern char func_80219E08_5D52D8;
extern M2C_UNK func_08001AEC_6B0EFC;

void func_08001A54_6B0E64(void *arg0, void *arg1) {
    func_08001A18_6B0E28(arg0);
    M2C_FIELD(arg0, s8 *, 0x6C) = 0;
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x2F1;
    ((M2C_UNK (*)(void *, M2C_UNK))&func_80216DF8_5D22C8)(arg0, 0);
    M2C_FIELD(arg1, f32 *, 8) = 15.0f;
    M2C_FIELD(arg1, f32 *, 0xC) = -52.0f;
    M2C_FIELD(arg1, f32 *, 0x10) = -18.0f;
    ((M2C_UNK (*)(void *, M2C_UNK))&func_80219E08_5D52D8)(arg0, 0x3F666666);
    ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08001AEC_6B0EFC);
}
