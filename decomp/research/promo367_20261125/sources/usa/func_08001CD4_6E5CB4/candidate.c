#include "m2c_types.h"
extern char func_8000F420_10020;
extern char func_8003521C_35E1C;
extern char func_802197D8_5D4CA8;
M2C_UNK func_08001D38_6E5D18();                     /* static */
extern M2C_UNK D_8020CBF0_5C8B00;

void func_08001CD4_6E5CB4(M2C_UNK arg0, s32 arg1) {
    if (((s32(*)())&func_802197D8_5D4CA8)(arg0, 6) == 0) {
        ((M2C_UNK(*)())&func_8000F420_10020)(0x261, &D_8020CBF0_5C8B00, arg1, 0x43C80000);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08001D38_6E5D18);
    }
}
