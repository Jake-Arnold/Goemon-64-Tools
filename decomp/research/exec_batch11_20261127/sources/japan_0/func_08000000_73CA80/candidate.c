#include "m2c_types.h"

extern u8 func_80014480_15080[];
extern u8 func_80034E8C_35A8C[];
extern s32 g_system_ptr;
extern u8 func_08000064_73CAE4[];

void func_08000000_73CA80(void *arg0, s32 arg1) {
    s32 *temp_v0;

    temp_v0 = ((s32 *(*)(s32, s32))func_80014480_15080)(g_system_ptr + 0xC7FA4, 0x38);
    M2C_FIELD(arg0, s32 **, 0xD0) = temp_v0;
    *temp_v0 = 0;
    ((void (*)(void *))func_80034E8C_35A8C)(func_08000064_73CAE4);
}
