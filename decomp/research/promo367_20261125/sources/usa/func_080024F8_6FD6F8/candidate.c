#include "m2c_types.h"
extern char func_80003E10_4A10;
extern char func_8003521C_35E1C;
M2C_UNK func_08002578_6FD778();                     /* static */

void func_080024F8_6FD6F8(void *arg0, void *arg1) {
    M2C_FIELD(arg1, f32 *, 0xC) = (f32) ((f32) (((f32(*)())&func_80003E10_4A10)(M2C_FIELD(arg0, u16 *, 0xD8)) * 20.0f) + M2C_FIELD(arg0, s16 *, 0xD0));
    if (M2C_FIELD(arg1, f32 *, 0x10) > 230.0f) {
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08002578_6FD778);
    }
}
