#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_802268B8_5E1E48;
extern char func_80229A50_5E4FE0;
M2C_UNK func_080002EC_72023C();                     /* static */
extern M2C_UNK D_8001DB0;
extern M2C_UNK D_8002DB0;
extern M2C_UNK D_8003DB0;

void func_08000284_7201D4(s32 arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_802268B8_5E1E48)();
    ((M2C_UNK(*)())&func_80229A50_5E4FE0)(arg0, &D_8001DB0, &D_8002DB0, &D_8003DB0);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080002EC_72023C);
}
