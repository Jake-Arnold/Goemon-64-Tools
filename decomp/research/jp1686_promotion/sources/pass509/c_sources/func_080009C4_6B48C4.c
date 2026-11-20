#include "m2c_types.h"
extern char func_80023D9C_2499C;
extern char func_80034B44_35744;
extern char func_80034E8C_35A8C;
extern char func_8022697C_5E1F0C;
M2C_UNK func_080004E8_6B43E8(void *, M2C_UNK);      /* static */
M2C_UNK func_08000588_6B4488();                     /* static */
extern M2C_UNK g_system;

void func_080009C4_6B48C4(void *arg0, M2C_UNK arg1) {
    if ((M2C_FIELD(&g_system, u16 *, 0x3ADF2) == 0x1B0) && (((s32(*)())&func_80023D9C_2499C)(0x17) != 0)) {
        ((M2C_UNK(*)())&func_80034B44_35744)();
        return;
    }
    func_080004E8_6B43E8(arg0, 0x12800761);
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x31B;
    ((M2C_UNK(*)())&func_8022697C_5E1F0C)(arg0, 3, 0x3E800000, 1);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08000588_6B4488);
}
