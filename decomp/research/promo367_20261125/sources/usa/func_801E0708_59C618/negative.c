#include "m2c_types.h"
extern char func_8001B5AC_1C1AC;
M2C_UNK func_801DACDC_596BEC(s32, M2C_UNK);
M2C_UNK func_801DD720_599630(s32, M2C_UNK);
M2C_UNK func_801E6F00_5A2E10(s32);
extern void *D_801FC61C_5B852C;
extern s32 D_801FC7C4_5B86D4;

void func_801E0708_59C618(s32 arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    M2C_FIELD(D_801FC61C_5B852C, s8 *, 0x64) = 1;
    D_801FC7C4_5B86D4 = 0;
    func_801DD720_599630(arg0, 5);
    if ((((f32(*)())&func_8001B5AC_1C1AC)(arg1) - 1.0f) <= M2C_FIELD(arg1, f32 *, 0x28)) {
        func_801E6F00_5A2E10(arg0);
        func_801DACDC_596BEC(arg0, 0);
    }
}
