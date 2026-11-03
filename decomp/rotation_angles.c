#include "common.h"
void func_8001F878_20478(u16 *arg0, u16 *arg1, u16 *arg2) {
    *arg1 = (0x200 - *arg1) & 0x3FF;
    *arg0 = (*arg0 + 0x200) & 0x3FF;
    *arg2 = (*arg2 + 0x200) & 0x3FF;
}
#pragma GLOBAL_ASM("asm/usa/nonmatchings/rotation_angles/func_8001F8B0_204B0.s")
#pragma GLOBAL_ASM("asm/usa/nonmatchings/rotation_angles/func_8001F914_20514.s")
#pragma GLOBAL_ASM("asm/usa/nonmatchings/rotation_angles/func_8001F940_20540.s")
#pragma GLOBAL_ASM("asm/usa/nonmatchings/rotation_angles/func_8001FA3C_2063C.s")
#pragma GLOBAL_ASM("asm/usa/nonmatchings/rotation_angles/func_8001FA80_20680.s")
