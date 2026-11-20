#include "m2c_types.h"
M2C_UNK func_800037A4_43A4();                       /* extern */
M2C_UNK func_80014450_15050(s32, M2C_UNK *, M2C_UNK); /* extern */
extern M2C_UNK D_802F7000;
extern s32 g_system_ptr;

void func_80003760_4360(void) {
    func_800037A4_43A4();
    func_80014450_15050(g_system_ptr + 0xC7FA4, &D_802F7000, 0xA000);
}
