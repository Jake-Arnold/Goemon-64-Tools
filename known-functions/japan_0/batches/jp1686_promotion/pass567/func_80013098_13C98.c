#include "../m2c_types.h"
void func_80013098_13C98(void *arg0) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x1C);
    M2C_FIELD(temp_v0, u8 *, 4) = (u8) (M2C_FIELD(temp_v0, u8 *, 4) | 0x80);
}
