#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80221F70_5DD440;
M2C_UNK func_08000220_7266B0();                     /* static */
s32 func_08002B30_728FC0();                         /* static */
extern void *D_801FC604_5B8514;

void func_080001AC_72663C(void *arg0, M2C_UNK arg1) {
    if ((M2C_FIELD(D_801FC604_5B8514, u8 *, 0x4C) == 0x1E) && (func_08002B30_728FC0() != 0)) {
        ((M2C_UNK(*)())&func_80221F70_5DD440)();
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x1E;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08000220_7266B0);
    }
}
