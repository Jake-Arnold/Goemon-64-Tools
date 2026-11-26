#include "m2c_types.h"
extern s32 D_801C7740_1C8340;
extern void *D_801FC628_5B8538;

void func_80214B90_5D0060(void) {
    void *ptr = (void *)(M2C_FIELD(D_801FC628_5B8538, u32 *, 0x2C) & 0x8FFFFFFE);
    M2C_FIELD(ptr, s16 *, 0x1A) = (s16) (D_801C7740_1C8340 * 4);
}
