#include "m2c_types.h"
void func_8021F080_5DA610(void *arg0) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x18);
    M2C_FIELD(temp_v0, u16 *, 0x14) = 0x8000;
    M2C_FIELD(temp_v0, u16 *, 0x16) = 0x8000;
    M2C_FIELD(temp_v0, u16 *, 0x18) = 0x8000;
}
