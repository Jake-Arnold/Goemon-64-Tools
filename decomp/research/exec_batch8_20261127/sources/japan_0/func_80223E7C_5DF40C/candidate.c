#include "m2c_types.h"
void func_80223BC0_5DF150(void *, u16, s32, s32, f32, s32);

void func_80223E7C_5DF40C(void *arg0, u16 arg1, s32 arg2) {
    void *temp_v0 = M2C_FIELD(arg0, void **, 0x84);
    func_80223BC0_5DF150(arg0, arg1, M2C_FIELD(temp_v0, s32 *, 8), M2C_FIELD(temp_v0, s32 *, 0xC), M2C_FIELD(temp_v0, f32 *, 0x10), arg2);
}
