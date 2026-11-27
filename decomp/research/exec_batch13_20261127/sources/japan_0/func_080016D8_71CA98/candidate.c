#include "m2c_types.h"

extern u8 func_8022697C_5E1F0C[];
extern u8 func_8003CFF8_3DBF8[];
extern u8 func_80034E8C_35A8C[];
extern u8 func_08001754_71CB14[];

void func_080016D8_71CA98(void *arg0, M2C_UNK arg1) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0xEC);
    if (M2C_FIELD(temp_v0, u8 *, 0xCD) == 3) {
        M2C_FIELD(temp_v0, u8 *, 0xCD) = 4;
        ((void (*)(void *, s32, s32, s32))func_8022697C_5E1F0C)(arg0, 0, 0x3F000000, 1);
        ((void (*)(u16, s32))func_8003CFF8_3DBF8)(M2C_FIELD(arg0, u16 *, 0xA4), 1);
        ((void (*)(void *))func_80034E8C_35A8C)(func_08001754_71CB14);
    }
}
