#include "m2c_types.h"
extern char func_80013B14_14714;
extern char func_800141C4_14DC4;
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
extern M2C_UNK func_0800079C_73CDAC;

void func_08000718_73CD28(void *arg0, M2C_UNK arg1) {
    s32 temp_v0 = M2C_FIELD(arg0, s32 *, 0xD0);
    M2C_FIELD(arg0, s32 *, 0xD0) = temp_v0;
    M2C_FIELD(arg0, s16 *, 0xDC) = ((s16(*)())&func_800240DC_24CDC)(0x1A, arg0);
    if (((s32(*)())&func_800141C4_14DC4)(0x18F, arg0) == -1) {
        ((M2C_UNK(*)())&func_80013B14_14714)(0x18F);
    }
    ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_0800079C_73CDAC);
}
