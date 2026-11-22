#include "../m2c_types.h"
M2C_UNK func_80014704_15304(s32, s32);              /* extern */
M2C_UNK func_80034B68_35768(void *);                /* extern */
extern s32 g_system_ptr;

void func_80217C70_69F370(void *arg0) {
    func_80014704_15304(g_system_ptr + 0xC7FA4, M2C_FIELD(arg0, s32 *, 0x5C));
    func_80034B68_35768(arg0);
}
