#include "../m2c_types.h"
s32 func_80034A48_35648(M2C_UNK *, M2C_UNK);        /* extern */
M2C_UNK func_801FE138_5BA108();                     /* static */
extern s16 D_80072E04_73A04;
extern M2C_UNK func_800203F4_20FF4;
extern M2C_UNK g_system;

void func_801FE0F8_5BA0C8(void) {
    D_80072E04_73A04 = 0x42;
    M2C_FIELD(&g_system, s32 *, 0xCF8B8) = func_80034A48_35648(&func_800203F4_20FF4, 0);
    func_801FE138_5BA108();
}
