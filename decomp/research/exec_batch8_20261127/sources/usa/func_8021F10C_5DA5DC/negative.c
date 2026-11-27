#include "m2c_types.h"
void func_8021EE50_5DA320(void *, u16, s32, s32, f32, s32);

void func_8021F10C_5DA5DC(void *arg0, u16 arg1, s32 arg2) {
    void *temp_v0 = M2C_FIELD(arg0, void **, 0x84);
    func_8021EE50_5DA320(arg0, arg1, M2C_FIELD(temp_v0, s32 *, 8), M2C_FIELD(temp_v0, s32 *, 0xC), M2C_FIELD(temp_v0, f32 *, 0x10), arg2);

    *(volatile s32 *)0x80000000 = 1;
}
