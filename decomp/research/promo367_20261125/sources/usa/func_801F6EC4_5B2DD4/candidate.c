#include "m2c_types.h"
extern char func_8001B5AC_1C1AC;
M2C_UNK func_801DACDC_596BEC(s32, M2C_UNK);
M2C_UNK func_801E7F50_5A3E60();
M2C_UNK func_801F70DC_5B2FEC(s32);

void func_801F6EC4_5B2DD4(s32 arg0, void *arg1) {
    func_801E7F50_5A3E60();
    if ((((f32(*)())&func_8001B5AC_1C1AC)(arg1) - 1.0f) <= M2C_FIELD(arg1, f32 *, 0x28)) {
        func_801F70DC_5B2FEC(arg0);
        func_801DACDC_596BEC(arg0, 0xB3);
    }
}
