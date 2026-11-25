#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80216DF8_5D22C8;
M2C_UNK func_08001A18_6B0E28();                     /* static */
M2C_UNK func_08001AEC_6B0EFC();                     /* static */

void func_08001BEC_6B0FFC(void *arg0, void *arg1) {
    func_08001A18_6B0E28();
    M2C_FIELD(arg0, s8 *, 0x6C) = 0;
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x2F2;
    ((M2C_UNK(*)())&func_80216DF8_5D22C8)(arg0, 0);
    M2C_FIELD(arg1, s16 *, 0x18) = 0;
    M2C_FIELD(arg1, s16 *, 0x16) = 0;
    M2C_FIELD(arg1, s16 *, 0x14) = 0;
    M2C_FIELD(arg1, f32 *, 8) = 50.0f;
    M2C_FIELD(arg1, f32 *, 0xC) = -47.0f;
    M2C_FIELD(arg1, f32 *, 0x10) = -8.0f;
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08001AEC_6B0EFC);
}
