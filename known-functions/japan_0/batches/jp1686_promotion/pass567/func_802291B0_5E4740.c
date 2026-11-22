#include "../m2c_types.h"
extern s32 g_system_ptr;

void func_802291B0_5E4740(s32 arg0) {
    s32 temp_v0;

    temp_v0 = arg0 * 0x18;
    M2C_FIELD((g_system_ptr + temp_v0), s16 *, 0x3B0F2) = 0;
    M2C_FIELD((g_system_ptr + temp_v0), s16 *, 0x3B0F4) = 0;
    M2C_FIELD((g_system_ptr + temp_v0), s16 *, 0x3B0F6) = 0;
    M2C_FIELD((g_system_ptr + temp_v0), s16 *, 0x3B0F8) = 0;
}
