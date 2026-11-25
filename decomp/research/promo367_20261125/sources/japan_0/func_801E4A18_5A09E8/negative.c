#include "m2c_types.h"
extern char func_8001B13C_1BD3C;
M2C_UNK func_801E019C_59C16C(s32, M2C_UNK);
s32 func_801E4B28_5A0AF8(s32);
M2C_UNK func_801E4B88_5A0B58(s32);
M2C_UNK func_801E70B8_5A3088(s32);
M2C_UNK func_801E8424_5A43F4(s32);
M2C_UNK func_801ED058_5A9028();

void func_801E4A18_5A09E8(s32 arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    func_801ED058_5A9028();
    func_801E8424_5A43F4(arg0);
    func_801E70B8_5A3088(arg0);
    if (func_801E4B28_5A0AF8(arg0) == 0) {
        if ((((f32(*)())&func_8001B13C_1BD3C)(arg1) - 1.0f) <= M2C_FIELD(arg1, f32 *, 0x28)) {
            func_801E019C_59C16C(arg0, 0x43);
            return;
        }
        func_801E4B88_5A0B58(arg0);
    }
}
