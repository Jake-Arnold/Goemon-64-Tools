#include "m2c_types.h"
extern char func_80023E94_24A94;
extern char func_80034ED4_35AD4;
extern char func_8003521C_35E1C;
extern char func_80221F70_5DD440;
M2C_UNK func_080001BC_73494C();                     /* static */
extern void *D_801FC624_5B8534;

void func_08000138_7348C8(s32 arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (((s32(*)())&func_80023E94_24A94)(0) != 0) {
        if (M2C_FIELD(D_801FC624_5B8534, u8 *, 0x61) != 0) {
            ((M2C_UNK(*)())&func_80034ED4_35AD4)();
            return;
        }
        ((M2C_UNK(*)())&func_80221F70_5DD440)();
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080001BC_73494C);
    }
}
