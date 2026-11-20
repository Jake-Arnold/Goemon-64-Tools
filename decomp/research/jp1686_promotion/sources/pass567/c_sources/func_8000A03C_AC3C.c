#include "../m2c_types.h"
extern M2C_UNK g_system;

void func_8000A03C_AC3C(void) {
    M2C_FIELD(&g_system, s16 *, 0xC5D0C) = 0xFF;
    M2C_FIELD(&g_system, s32 *, 0xC5D10) = 0;
    M2C_FIELD(&g_system, s16 *, 0xC5D0A) = (s16) M2C_FIELD(&g_system, s16 *, 0xC5D0C);
    M2C_FIELD(&g_system, s16 *, 0xC5D08) = (s16) M2C_FIELD(&g_system, s16 *, 0xC5D0A);
    M2C_FIELD(&g_system, s16 *, 0xC5D06) = (s16) M2C_FIELD(&g_system, s16 *, 0xC5D08);
}
