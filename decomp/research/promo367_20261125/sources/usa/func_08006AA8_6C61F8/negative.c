#include "m2c_types.h"
extern char func_8003521C_35E1C;
M2C_UNK func_08006B00_6C6250();                     /* static */

void func_08006AA8_6C61F8(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (M2C_FIELD(arg1, f32 *, 0x10) == 396.0f) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x3C;
        M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08006B00_6C6250);
    }
}
