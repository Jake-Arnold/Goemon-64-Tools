#include "m2c_types.h"
extern char func_80023D48_24948;
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
extern char func_80036D58_37958;
extern char func_80036E24_37A24;
extern char func_80226A3C_5E1FCC;
extern M2C_UNK func_80035124_35D24;
extern M2C_UNK g_system;

void func_08001554_6B5454(void *arg0, void *arg1) {
    if (M2C_FIELD(arg0, s32 *, 0x68) & 0x100) {
        ((M2C_UNK(*)())&func_80226A3C_5E1FCC)();
    } else {
        M2C_FIELD(arg1, u16 *, 0x7E) = (u16) M2C_FIELD(arg0, u16 *, 0xA8);
    }
    if (((s32(*)())&func_80023D9C_2499C)(0x79) != 0) {
        ((M2C_UNK(*)())&func_80023D48_24948)(0x79);
        if (M2C_FIELD(&g_system, u16 *, 0x3ADF4) == 0x3F) {
            ((M2C_UNK(*)())&func_80036D58_37958)();
        } else {
            ((M2C_UNK(*)())&func_80036E24_37A24)();
        }
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_80035124_35D24);
    }
}
