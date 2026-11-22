#include "../m2c_types.h"
extern M2C_UNK g_system;

void func_80008574_9174(void *arg0, s32 arg1, s32 arg2) {
    M2C_FIELD(arg0, s32 *, 0x34) = arg1;
    M2C_FIELD(arg0, s32 *, 0x14) = arg2;
    M2C_FIELD(&g_system, s32 *, 0xC5F78) = arg2;
}
