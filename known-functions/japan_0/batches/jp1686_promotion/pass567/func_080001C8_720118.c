#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_802268B8_5E1E48;
extern char func_80229A50_5E4FE0;
M2C_UNK func_08000230_720180();                     /* static */
extern M2C_UNK D_80025B0;
extern M2C_UNK D_80035B0;
extern M2C_UNK D_80045B0;

void func_080001C8_720118(s32 arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_802268B8_5E1E48)();
    ((M2C_UNK(*)())&func_80229A50_5E4FE0)(arg0, &D_80025B0, &D_80045B0, &D_80035B0);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08000230_720180);
}
