#include "m2c_types.h"
extern char func_80226060_5E15F0;

void func_08001AD8_6B59D8(void *arg0, M2C_UNK arg1) {
    void *temp_v0;

    if (M2C_FIELD(arg0, s32 *, 0xE0) != 0) {
        temp_v0 = M2C_FIELD(arg0, void **, 0xE8);
        M2C_FIELD(temp_v0, s32 *, 0x68) = (s32) (M2C_FIELD(temp_v0, s32 *, 0x68) & ~0x100);
        M2C_FIELD(arg0, s32 *, 0xE0) = 0;
        return;
    }
    if (((s32(*)())&func_80226060_5E15F0)() != 0) {
        M2C_FIELD(M2C_FIELD(arg0, void **, 0xE8), s32 *, 0x68) = 0x100;
        M2C_FIELD(arg0, s32 *, 0xE0) = 1;
    }
}
