#include "m2c_types.h"
M2C_UNK func_80014704_15304(s32, s32, void *);      /* extern */
M2C_UNK func_80034B68_35768(void *);                /* extern */
extern s32 g_system_ptr;

void func_80215FE4_674E54(void *arg0) {
    s32 temp_a1;

    if (arg0 != NULL) {
        temp_a1 = M2C_FIELD(arg0, s32 *, 0x5C);
        if (temp_a1 != 0) {
            func_80014704_15304(g_system_ptr + 0xC7FA4, temp_a1, arg0);
        }
        func_80034B68_35768(arg0);
    }
}
