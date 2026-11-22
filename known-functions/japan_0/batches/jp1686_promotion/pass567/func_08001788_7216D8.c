#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_802268B8_5E1E48;
extern char func_80229A50_5E4FE0;
M2C_UNK func_080017F0_721740();                     /* static */
extern M2C_UNK D_8002010;
extern M2C_UNK D_8003010;
extern M2C_UNK D_8004010;

void func_08001788_7216D8(s32 arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_802268B8_5E1E48)();
    ((M2C_UNK(*)())&func_80229A50_5E4FE0)(arg0, &D_8002010, &D_8004010, &D_8003010);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080017F0_721740);
}
