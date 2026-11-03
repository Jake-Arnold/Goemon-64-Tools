#include "common.h"
void func_80003380_3F80(s32);
void func_80003428_4028(u8);
void func_80003528_4128(u8);
void func_80003628_4228(u8);
#pragma GLOBAL_ASM("asm/usa/nonmatchings/transition_state/func_80003380_3F80.s")
#pragma GLOBAL_ASM("asm/usa/nonmatchings/transition_state/func_800033B0_3FB0.s")
#pragma GLOBAL_ASM("asm/usa/nonmatchings/transition_state/func_800033EC_3FEC.s")
void func_80003428_4028(u8 arg0) {
    D_8015C5C8_15D1C8->unk_3adde = arg0;
    D_8015C5C8_15D1C8->unk_3addf = 0;
    func_80003380_3F80(0);
}
#pragma GLOBAL_ASM("asm/usa/nonmatchings/transition_state/func_80003478_4078.s")
#pragma GLOBAL_ASM("asm/usa/nonmatchings/transition_state/func_800034D0_40D0.s")
void func_80003528_4128(u8 arg0) {
    D_8015C5C8_15D1C8->unk_3add8 = arg0;
    D_8015C5C8_15D1C8->unk_3add9 = 0;
    func_80003428_4028(0);
}
#pragma GLOBAL_ASM("asm/usa/nonmatchings/transition_state/func_80003578_4178.s")
#pragma GLOBAL_ASM("asm/usa/nonmatchings/transition_state/func_800035D0_41D0.s")
void func_80003628_4228(u8 arg0) {
    D_8015C5C8_15D1C8->unk_3add6 = arg0;
    D_8015C5C8_15D1C8->unk_3add7 = 0;
    func_80003528_4128(0);
}
#pragma GLOBAL_ASM("asm/usa/nonmatchings/transition_state/func_80003678_4278.s")
#pragma GLOBAL_ASM("asm/usa/nonmatchings/transition_state/func_800036D0_42D0.s")
void func_80003728_4328(u8 arg0) {
    D_8015C5C8_15D1C8->stepw = arg0;
    D_8015C5C8_15D1C8->stepw_end = 0;
    D_8015C5C8_15D1C8->retraces_per_game_step = 2;
    func_80003628_4228(0);
}
#pragma GLOBAL_ASM("asm/usa/nonmatchings/transition_state/func_8000378C_438C.s")
#pragma GLOBAL_ASM("asm/usa/nonmatchings/transition_state/func_800037E4_43E4.s")
#pragma GLOBAL_ASM("asm/usa/nonmatchings/transition_state/func_8000383C_443C.s")
#pragma GLOBAL_ASM("asm/usa/nonmatchings/transition_state/func_80003880_4480.s")
#pragma GLOBAL_ASM("asm/usa/nonmatchings/transition_state/func_800038E4_44E4.s")
#pragma GLOBAL_ASM("asm/usa/nonmatchings/transition_state/func_8000394C_454C.s")
