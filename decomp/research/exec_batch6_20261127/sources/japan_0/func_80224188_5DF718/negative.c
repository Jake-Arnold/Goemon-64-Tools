#include "m2c_types.h"
M2C_UNK func_8022406C_5DF5FC(void *, f32, u16, s32, f32, f32);

void func_80224188_5DF718(void *arg0, f32 arg1, u16 arg2) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x84);
    func_8022406C_5DF5FC(arg0, arg1, arg2, M2C_FIELD(temp_v0, s32 *, 8), M2C_FIELD(temp_v0, f32 *, 0xC), M2C_FIELD(temp_v0, f32 *, 0x10));

    *(volatile s32 *)0x80000000 = 1;
}
