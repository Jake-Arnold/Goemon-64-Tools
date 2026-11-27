#include "m2c_types.h"
M2C_UNK func_0800281C_6D876C(s32);                  /* extern */
extern char func_8021B09C_5D656C;
extern char func_8021C628_5D7AF8;
extern char func_8021D9A8_5D8E78;

void func_08003284_6D91D4(void *arg0, s32 arg1) {
    M2C_FIELD(arg0, s8 *, 0xDC) = 5;
    if (((s32  (*)(void *, M2C_UNK))&func_8021C628_5D7AF8)(arg0, 0x40000000) != 0) {
        func_0800281C_6D876C(arg1);
    }
    if (((s32 (*)(void *, u16, M2C_UNK))&func_8021D9A8_5D8E78)(arg0, M2C_FIELD(arg0, u16 *, 0xD0), 5) != 0) {
        ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK))&func_8021B09C_5D656C)(arg0, 0, 1);
    }

    *(volatile s32 *)0x80000000 = 1;
}
