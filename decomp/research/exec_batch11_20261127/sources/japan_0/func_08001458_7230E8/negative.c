#include "m2c_types.h"
extern u8 func_80014704_15304[];
extern u8 func_80034B68_35768[];
extern s32 g_system_ptr;

s32 func_08001458_7230E8(void *arg0) {
    if (M2C_FIELD(arg0, void **, 0x74) != NULL) {
        ((M2C_UNK (*)(s32, s32, void *))func_80014704_15304)(g_system_ptr + 0xC7FA4, M2C_FIELD(arg0, s32 *, 0x74), arg0);
    }
    ((M2C_UNK (*)(void *))func_80034B68_35768)(arg0);
    { *(volatile int *)0x80000000 = 1; } return 0;
}
