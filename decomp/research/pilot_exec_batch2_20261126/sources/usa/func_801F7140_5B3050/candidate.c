#include "m2c_types.h"
void func_801F7140_5B3050(void *arg0, f32 arg1) {
    void *temp_v0;
    f32 temp;

    temp_v0 = M2C_FIELD(arg0, void **, 0x5C);
    temp = (M2C_FIELD(temp_v0, f32 *, 0xAC) / 3.0f) * arg1;
    M2C_FIELD(temp_v0, f32 *, 0x1C) = M2C_FIELD(arg0, f32 *, 0xD0) * temp;
}
