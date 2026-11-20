#include "m2c_types.h"
extern char func_80011F10_12B10;
extern char func_80012030_12C30;
extern char func_800120A8_12CA8;
extern char func_800121B8_12DB8;
extern char func_80034E8C_35A8C;
M2C_UNK func_08000644_72AEF4();                     /* static */

void func_0800057C_72AE2C(void *arg0, M2C_UNK arg1) {
    void *temp_s0;

    temp_s0 = M2C_FIELD(arg0, void **, 0xD0);
    if (M2C_FIELD(arg0, u16 *, 0x8A) == 0) {
        ((M2C_UNK(*)())&func_80012030_12C30)(M2C_FIELD(temp_s0, s32 *, 0x18), 0x42480000);
        ((M2C_UNK(*)())&func_800120A8_12CA8)(M2C_FIELD(temp_s0, s32 *, 0x18), 0xC1100000, 0x43A20000, 0x43770000);
        ((M2C_UNK(*)())&func_800121B8_12DB8)(M2C_FIELD(temp_s0, s32 *, 0x18), 0xC0000000, 0x43968000, 0x43A10000);
    }
    if (((s32(*)())&func_80011F10_12B10)(M2C_FIELD(temp_s0, s32 *, 0x18)) == 0) {
        M2C_FIELD(arg0, u16 *, 0x8A) = 0U;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08000644_72AEF4);
        return;
    }
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (M2C_FIELD(arg0, u16 *, 0x8A) + 1);
}
