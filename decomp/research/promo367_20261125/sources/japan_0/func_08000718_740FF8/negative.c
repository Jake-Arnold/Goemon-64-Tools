#include "m2c_types.h"
extern char func_800136A4_142A4;
extern char func_80013D54_14954;
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
extern M2C_UNK func_0800079C_74107C;

void func_08000718_740FF8(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_v0 = M2C_FIELD(arg0, s32 *, 0xD0);
    M2C_FIELD(arg0, s32 *, 0xD0) = temp_v0;
    M2C_FIELD(arg0, s16 *, 0xDC) = ((s16(*)())&func_80023D9C_2499C)(0x1A, arg0);
    if (((s32(*)())&func_80013D54_14954)(0x18F, arg0) == -1) {
        ((M2C_UNK(*)())&func_800136A4_142A4)(0x18F);
    }
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_0800079C_74107C);
}
