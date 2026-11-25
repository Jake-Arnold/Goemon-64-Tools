#include "m2c_types.h"
extern char func_8001B5AC_1C1AC;
M2C_UNK func_801DACDC_596BEC(s32, M2C_UNK);
s32 func_801DF858_59B768(s32);
M2C_UNK func_801DF8B8_59B7C8(s32);
M2C_UNK func_801E1E70_59DD80(s32);
M2C_UNK func_801E31DC_59F0EC(s32);
M2C_UNK func_801E7F50_5A3E60();

void func_801DF748_59B658(s32 arg0, void *arg1) {
    func_801E7F50_5A3E60();
    func_801E31DC_59F0EC(arg0);
    func_801E1E70_59DD80(arg0);
    if (func_801DF858_59B768(arg0) == 0) {
        if ((((f32(*)())&func_8001B5AC_1C1AC)(arg1) - 1.0f) <= M2C_FIELD(arg1, f32 *, 0x28)) {
            func_801DACDC_596BEC(arg0, 0x43);
            return;
        }
        func_801DF8B8_59B7C8(arg0);
    }
}
