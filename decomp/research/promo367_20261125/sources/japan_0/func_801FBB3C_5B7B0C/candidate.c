#include "m2c_types.h"
extern char func_8001B13C_1BD3C;
M2C_UNK func_801E019C_59C16C(s32, M2C_UNK);
M2C_UNK func_801ED058_5A9028();
M2C_UNK func_801FBFC0_5B7F90(s32);

void func_801FBB3C_5B7B0C(s32 arg0, void *arg1) {
    func_801ED058_5A9028();
    if ((((f32(*)())&func_8001B13C_1BD3C)(arg1) - 1.0f) <= M2C_FIELD(arg1, f32 *, 0x28)) {
        func_801FBFC0_5B7F90(arg0);
        func_801E019C_59C16C(arg0, 0xB3);
    }
}
