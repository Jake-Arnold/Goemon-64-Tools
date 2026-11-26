#include "m2c_types.h"
extern char func_800148F0_154F0;
extern char func_80034ED4_35AD4;
extern char func_8003521C_35E1C;
M2C_UNK func_080000A8_734838();                     /* static */
M2C_UNK func_08003920_7380B0();                     /* static */
extern void *D_801FC628_5B8538;
extern s32 D_8015C5C8_15D1C8;

void func_08000000_734790(void *arg0, M2C_UNK arg1) {
volatile int negative_control=1;

    void *sp1C;
    void *temp_v0;

    temp_v0 = ((void *(*)())&func_800148F0_154F0)(D_8015C5C8_15D1C8 + 0xC7FA4, 0x68);
    M2C_FIELD(arg0, void **, 0xD0) = temp_v0;
    if (temp_v0 == NULL) {
        ((M2C_UNK(*)())&func_80034ED4_35AD4)();
        return;
    }
    sp1C = M2C_FIELD(arg0, void **, 0xD0);
    func_08003920_7380B0();
    M2C_FIELD(sp1C, s32 *, 0x60) = (s32) (M2C_FIELD(D_801FC628_5B8538, s32 *, 0x2C) & 0x8FFFFFFE);
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080000A8_734838);
}
