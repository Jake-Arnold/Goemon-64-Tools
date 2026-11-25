#include "m2c_types.h"
extern char func_8003521C_35E1C;
M2C_UNK func_08001B60_6C12B0();                     /* static */

void func_08001B04_6C1254(void *arg0, void *arg1) {
    M2C_FIELD(arg0, f32 *, 0x80) = 0.5f;
    if (!(M2C_FIELD(arg1, f32 *, 0x10) < 40.0f)) {
        M2C_FIELD(arg0, s32 *, 0x60) = 0x02A007E1;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08001B60_6C12B0);
    }
}
