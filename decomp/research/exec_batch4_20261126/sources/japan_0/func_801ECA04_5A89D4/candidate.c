#include "m2c_types.h"
void func_801E2848_59E818(void *);

void func_801ECA04_5A89D4(void *arg0) {
    void *temp_v0;
    u16 temp_v1;

    temp_v0 = M2C_FIELD(arg0, void **, 0x5C);
    temp_v1 = M2C_FIELD(temp_v0, u16 *, 0x86);
    if ((temp_v1 != 0) && (temp_v1 != 0xFFFF)) {
        M2C_FIELD(temp_v0, u16 *, 0x86) = temp_v1 - 1;
        temp_v0 = M2C_FIELD(arg0, void **, 0x5C);
        if ((M2C_FIELD(temp_v0, u16 *, 0x86) == 0) && (M2C_FIELD(arg0, u8 *, 0x60) == 0)) {
            M2C_FIELD(temp_v0, s8 *, 0x84) = 2;
            func_801E2848_59E818(arg0);
            M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s8 *, 0x84) = 0;
        }
    }
}
