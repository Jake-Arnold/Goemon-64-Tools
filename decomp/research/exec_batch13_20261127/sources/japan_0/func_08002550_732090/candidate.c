#include "m2c_types.h"

extern u8 *g_system_ptr;
extern u8 func_80014480_15080[];
extern u8 func_80034E8C_35A8C[];
extern u8 func_080014E8_731028[];

void func_08002550_732090(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;
    s32 var_v1;

    temp_v0 = ((s32 (*)(u8 *, s32))func_80014480_15080)(g_system_ptr + 0xC7FA4, 0x20);
    if (temp_v0 != 0) {
        M2C_FIELD(arg0, s32 *, 0xD0) = temp_v0;
        for (var_v1 = 0; var_v1 != 8; var_v1 += 4) {
        }
        ((void (*)(void *))func_80034E8C_35A8C)(func_080014E8_731028);
    }
}
