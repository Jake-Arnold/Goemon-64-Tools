#include "common.h"
extern u16 D_800C7A76_C8676;
extern s32 D_8006D328_6DF28;
void func_80020440_21040(void);
void func_80003478_4078(void);
void func_80004240_4E40(void);
void func_80034EF8_35AF8(s32);
void func_8001F878_20478(u16 *arg0, u16 *arg1, u16 *arg2) {
    *arg1 = (0x200 - *arg1) & 0x3FF;
    *arg0 = (*arg0 + 0x200) & 0x3FF;
    *arg2 = (*arg2 + 0x200) & 0x3FF;
}
#pragma GLOBAL_ASM("asm/usa/nonmatchings/rotation_angles/func_8001F8B0_204B0.s")
void func_8001F914_20514(void) {
    func_80020440_21040();
    D_800C7A76_C8676 = 0;
    func_80003478_4078();
}
#pragma GLOBAL_ASM("asm/usa/nonmatchings/rotation_angles/func_8001F940_20540.s")
void func_8001FA3C_2063C(void) {
    func_80004240_4E40();
    func_80034EF8_35AF8(D_8006D328_6DF28);
    D_8015C5C8_15D1C8->unk_3addf = 1;
}
#pragma GLOBAL_ASM("asm/usa/nonmatchings/rotation_angles/func_8001FA80_20680.s")
