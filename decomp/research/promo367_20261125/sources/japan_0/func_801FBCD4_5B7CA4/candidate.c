#include "m2c_types.h"
extern char func_8001B13C_1BD3C;
M2C_UNK func_801E019C_59C16C(void *, M2C_UNK);
M2C_UNK func_801ED058_5A9028();

void func_801FBCD4_5B7CA4(void *arg0, void *arg1) {
    func_801ED058_5A9028();
    if ((((f32(*)())&func_8001B13C_1BD3C)(arg1) - 1.0f) <= M2C_FIELD(arg1, f32 *, 0x28)) {
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), f32 *, 0xAC) = 0.0f;
        func_801E019C_59C16C(arg0, 0xAE);
    }
}
