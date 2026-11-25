#include "../m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80216DF8_5D22C8;
M2C_UNK func_08001A18_6B0E28();                     /* static */
M2C_UNK func_08001AEC_6B0EFC();                     /* static */

void func_08001F90_6B13A0(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    func_08001A18_6B0E28();
    M2C_FIELD(arg0, s8 *, 0x6C) = 0;
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x30C;
    ((M2C_UNK(*)())&func_80216DF8_5D22C8)(arg0, 0);
    M2C_FIELD(arg1, f32 *, 8) = 0.0f;
    M2C_FIELD(arg1, f32 *, 0xC) = 0.0f;
    M2C_FIELD(arg1, f32 *, 0x10) = 0.0f;
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08001AEC_6B0EFC);
}
