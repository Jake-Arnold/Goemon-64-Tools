#include "common.h"
void func_80003380_3F80(u8);
void func_80003428_4028(u8);
void func_80003528_4128(u8);
void func_80003628_4228(u8);
void func_8000B364_BF64(void);
extern char D_802F7000[];
void func_8000383C_443C(void);
void func_80003880_4480(void);
extern u8 D_800627F0_633F0[];
extern u16 D_800C7AE4_C86E4;
void func_80004240_4E40(void);
void func_8003488C_3548C(void *);
void func_8000A0F0_ACF0(void);
void func_80035B50_36750(void);
void func_8000B880_C480(void);
void func_8000B8A4_C4A4(void *);
void func_80013940_14540(void);
void osViBlack(u8);
void func_800148C0_154C0(void *, char *, u32);
void func_80003728_4328(u8);
void func_8001F8B0_204B0(void);
void func_80034734_35334(void);
extern u8 D_800C7A95_C8695;
extern s32 D_8006D328_6DF28;
void func_800369F0_375F0(s32);
void func_80038BC8_397C8(s32);
#pragma GLOBAL_ASM("asm/usa/nonmatchings/transition_state/func_800030F0_3CF0.s")
void func_80003328_3F28(void) {
    func_8000B364_BF64();
    func_8000383C_443C();
    func_80003728_4328(0x11);
}
void func_80003358_3F58(void) {
    func_8001F8B0_204B0();
    func_80034734_35334();
}
void func_80003380_3F80(u8 arg0) {
    D_8015C5C8_15D1C8->unk_3ade0 = arg0;
    D_8015C5C8_15D1C8->unk_3ade1 = 0;
}
void func_800033B0_3FB0(void) { D_8015C5C8_15D1C8->unk_3ade0++; D_8015C5C8_15D1C8->unk_3ade1=0;  }
void func_800033EC_3FEC(void) { D_8015C5C8_15D1C8->unk_3ade0--; D_8015C5C8_15D1C8->unk_3ade1=0;  }
void func_80003428_4028(u8 arg0) {
    D_8015C5C8_15D1C8->unk_3adde = arg0;
    D_8015C5C8_15D1C8->unk_3addf = 0;
    func_80003380_3F80(0);
}
void func_80003478_4078(void) { D_8015C5C8_15D1C8->unk_3adde++; D_8015C5C8_15D1C8->unk_3addf=0; func_80003380_3F80(0); }
void func_800034D0_40D0(void) { D_8015C5C8_15D1C8->unk_3adde--; D_8015C5C8_15D1C8->unk_3addf=0; func_80003380_3F80(0); }
void func_80003528_4128(u8 arg0) {
    D_8015C5C8_15D1C8->unk_3add8 = arg0;
    D_8015C5C8_15D1C8->unk_3add9 = 0;
    func_80003428_4028(0);
}
void func_80003578_4178(void) { D_8015C5C8_15D1C8->unk_3add8++; D_8015C5C8_15D1C8->unk_3add9=0; func_80003428_4028(0); }
void func_800035D0_41D0(void) { D_8015C5C8_15D1C8->unk_3add8--; D_8015C5C8_15D1C8->unk_3add9=0; func_80003428_4028(0); }
void func_80003628_4228(u8 arg0) {
    D_8015C5C8_15D1C8->unk_3add6 = arg0;
    D_8015C5C8_15D1C8->unk_3add7 = 0;
    func_80003528_4128(0);
}
void func_80003678_4278(void) { D_8015C5C8_15D1C8->unk_3add6++; D_8015C5C8_15D1C8->unk_3add7=0; func_80003528_4128(0); }
void func_800036D0_42D0(void) { D_8015C5C8_15D1C8->unk_3add6--; D_8015C5C8_15D1C8->unk_3add7=0; func_80003528_4128(0); }
void func_80003728_4328(u8 arg0) {
    D_8015C5C8_15D1C8->stepw = arg0;
    D_8015C5C8_15D1C8->stepw_end = 0;
    D_8015C5C8_15D1C8->retraces_per_game_step = 2;
    func_80003628_4228(0);
}
void func_8000378C_438C(void) { D_8015C5C8_15D1C8->stepw++; D_8015C5C8_15D1C8->stepw_end=0; func_80003628_4228(0); }
void func_800037E4_43E4(void) { D_8015C5C8_15D1C8->stepw--; D_8015C5C8_15D1C8->stepw_end=0; func_80003628_4228(0); }
void func_8000383C_443C(void) {
    func_80003880_4480();
    func_800148C0_154C0((u8 *) D_8015C5C8_15D1C8 + 0xC7FA4, D_802F7000, 0xA000);
}
void func_80003880_4480(void) {
    func_80004240_4E40();
    func_8003488C_3548C(0);
    func_8000A0F0_ACF0();
    func_80035B50_36750();
    func_8000B880_C480();
    func_8000B8A4_C4A4(D_800627F0_633F0);
    D_800C7AE4_C86E4 = 20;
    func_80013940_14540();
    osViBlack(0);
}
void func_800038E4_44E4(void) {
    func_80034734_35334();
    if (D_800C7A95_C8695 != 0) {
        func_800369F0_375F0(D_8006D328_6DF28);
        D_8015C5C8_15D1C8->unk_3add6++;
        func_80038BC8_397C8(7);
    }
}
#pragma GLOBAL_ASM("asm/usa/nonmatchings/transition_state/func_8000394C_454C.s")
