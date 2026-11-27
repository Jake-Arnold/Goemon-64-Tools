#include "m2c_types.h"
extern u8 func_80034E8C_35A8C[];
extern u8 func_802268B8_5E1E48[];
extern u8 D_3B07A[];
extern s32 g_system_ptr;
extern M2C_UNK func_08000150_7200A0;

void func_080000E8_720038(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, s32 *, 0xD8) != 1 || *(u16 *)(D_3B07A + g_system_ptr) == 0xC00F) {
        ((M2C_UNK (*)(void))func_802268B8_5E1E48)();
        ((M2C_UNK (*)(M2C_UNK *))func_80034E8C_35A8C)(&func_08000150_7200A0);
    }
}
