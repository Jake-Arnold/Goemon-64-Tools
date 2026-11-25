#include "m2c_types.h"
M2C_UNK func_080004FC_6AF90C(void *, M2C_UNK);
extern char func_800240DC_24CDC;
extern char func_80034ED4_35AD4;
extern char func_8003521C_35E1C;
extern char func_80221C0C_5DD0DC;
extern u16 D_800C7AB2;
extern M2C_UNK func_0800059C_6AF9AC;

void func_080009D8_6AFDE8(void *arg0, M2C_UNK arg1) {
    if ((D_800C7AB2 == 0x1B0) && (((s32(*)())&func_800240DC_24CDC)(0x17) != 0)) {
        ((M2C_UNK(*)())&func_80034ED4_35AD4)();
        return;
    }
    func_080004FC_6AF90C(arg0, 0x12800761);
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x31B;
    ((M2C_UNK(*)())&func_80221C0C_5DD0DC)(arg0, 3, 0x3E800000, 1);
    ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_0800059C_6AF9AC);
}
