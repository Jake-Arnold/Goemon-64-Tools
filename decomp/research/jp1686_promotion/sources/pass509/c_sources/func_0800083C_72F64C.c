#include "m2c_types.h"
extern char func_80014704_15304;
extern char func_80034B44_35744;
extern char func_8003EE44_3FA44;
extern s32 g_system_ptr;

void func_0800083C_72F64C(void *arg0, M2C_UNK arg1) {
    s32 sp1C;

    sp1C = M2C_FIELD(arg0, s32 *, 0xD0);
    if (((s32(*)())&func_8003EE44_3FA44)() == 0) {
        ((M2C_UNK(*)())&func_80014704_15304)(g_system_ptr + 0xC7FA4, sp1C);
        ((M2C_UNK(*)())&func_80034B44_35744)();
    }
}
