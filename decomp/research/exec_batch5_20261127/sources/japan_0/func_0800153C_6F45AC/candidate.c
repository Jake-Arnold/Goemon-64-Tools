#include "m2c_types.h"

void func_0800153C_6F45AC(void *arg0) {
    void *temp_v0;
    void *temp_v1;
    void *temp_a1;

    temp_v0 = M2C_FIELD(arg0, void **, 0x18);
    temp_v1 = M2C_FIELD(arg0, void **, 0xD0);
    temp_a1 = M2C_FIELD(temp_v1, void **, 0x18);
    M2C_FIELD(temp_v0, f32 *, 8) = M2C_FIELD(temp_a1, f32 *, 8);
    M2C_FIELD(temp_v0, f32 *, 0xC) = M2C_FIELD(temp_a1, f32 *, 0xC);
    M2C_FIELD(temp_v0, f32 *, 0x10) = M2C_FIELD(temp_a1, f32 *, 0x10);
    M2C_FIELD(temp_v0, u16 *, 0x14) = M2C_FIELD(temp_a1, u16 *, 0x14);
    M2C_FIELD(temp_v0, u16 *, 0x16) = M2C_FIELD(temp_a1, u16 *, 0x16);
    M2C_FIELD(temp_v0, u16 *, 0x18) = M2C_FIELD(temp_a1, u16 *, 0x18);
}
