#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_802268B8_5E1E48;
extern char func_80229A50_5E4FE0;
M2C_UNK func_08001678_7215C8();                     /* static */
extern M2C_UNK D_8002090;
extern M2C_UNK D_8003090;
extern M2C_UNK D_8004090;

void func_08001610_721560(s32 arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_802268B8_5E1E48)();
    ((M2C_UNK(*)())&func_80229A50_5E4FE0)(arg0, &D_8002090, &D_8003090, &D_8004090);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001678_7215C8);
}
