#include "m2c_types.h"
extern u8 func_8003521C_35E1C[];
extern u8 func_8021C628_5D7AF8[];
extern u8 func_08002F58_6D2038[];

void func_08002EF4_6D1FD4(void *arg0, M2C_UNK arg1) {
    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        ((void (*)(void *, f32))func_8021C628_5D7AF8)(arg0, 4.0f / 3.0f);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x14;
        ((void (*)(void *))func_8003521C_35E1C)(func_08002F58_6D2038);
    }
}
