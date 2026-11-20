#include "m2c_types.h"
void func_801DB7D4_606254(void *arg0) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x18);
    M2C_FIELD(temp_v0, f32 *, 0xC) = (f32) (M2C_FIELD(arg0, f32 *, 0x74) + M2C_FIELD(temp_v0, f32 *, 0xC));
}
