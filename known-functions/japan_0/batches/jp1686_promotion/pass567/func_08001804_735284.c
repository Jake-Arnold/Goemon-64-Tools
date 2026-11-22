#include "../m2c_types.h"
extern char func_80014704_15304;
extern char func_80034B68_35768;
extern s32 g_system_ptr;

void func_08001804_735284(void *arg0) {
    ((M2C_UNK(*)())&func_80014704_15304)(g_system_ptr + 0xC7FA4, M2C_FIELD(arg0, s32 *, 0xEC));
    ((M2C_UNK(*)())&func_80034B68_35768)(arg0);
}
