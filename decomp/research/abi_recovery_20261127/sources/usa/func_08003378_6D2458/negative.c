#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_802196E4_5D4BB4;
extern char func_8021B424_5D68F4;
extern M2C_UNK func_0800342C_6D250C;

void func_08003378_6D2458(void *arg0, void *arg1) {
    ((M2C_UNK (*)())&func_802196E4_5D4BB4)();
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_8021664C_5D1B1C)(arg0, 0, 0x3F000000, 1);
    ((M2C_UNK (*)(void *, u16, f32))&func_8021B424_5D68F4)(arg0, M2C_FIELD(arg1, u16 *, 0x16), (f32) ((f64) (f32) M2C_FIELD(arg0, s16 *, 0xD2) / 10.0));
    M2C_FIELD(arg0, s16 *, 0xDC) = 0;
    M2C_FIELD(arg0, u16 *, 0xDE) = (u16) M2C_FIELD(arg0, u16 *, 0xD4);
    ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_0800342C_6D250C);

    *(volatile s32 *)0x80000000 = 1;
}
