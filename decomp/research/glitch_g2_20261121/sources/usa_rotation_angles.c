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
typedef void (*GlitchFn)(void);
typedef struct { GlitchFn a,b,c; } GlitchTable;
extern GlitchTable D_8006B730_6C330;
extern u8 D_3ADDE[];
void func_8001F8B0_204B0(void) {
    GlitchTable cbs = D_8006B730_6C330;
    ((GlitchFn*)&cbs)[((u8*)D_8015C5C8_15D1C8)[(u32)D_3ADDE]]();
}
void func_8001F914_20514(void) {
    func_80020440_21040();
    D_800C7A76_C8676 = 0;
    func_80003478_4078();
}
typedef struct GlitchSys {
char pad_0[0xADE0];
s8 phase;
s8 phase_b;
char pad_3ADE2[0x2];
u8 submode;
char pad_3ADE5[0x31];
u16 condition;
char pad_3AE18[0xE];
u16 pause_latch;
char pad_3AE28[0x1];
u8 local_gate;
char pad_3AE2A[0x252];
} GlitchSys;
typedef struct GlitchExt {char pad_0[0xF88D]; u8 external_b; char pad_CF88E[0x14];u8 external_a;} GlitchExt;
extern GlitchExt D_8014CCC0_14D8C0;
extern GlitchSys D_800BCCC0_BD8C0;
extern u16 D_800C7D3C_C893C;
void func_8000B7E4_C3E4(void);
void func_8001FA80_20680(void);
void func_80038BC8_397C8(s32);
s32 func_8003F1D8_3FDD8(void);
void func_8001F940_20540(void) {
    func_8000B7E4_C3E4();
    if (D_800BCCC0_BD8C0.pause_latch == 0) {
        if ((D_800C7D3C_C893C & 0x1000) && (D_800BCCC0_BD8C0.local_gate == 0) && (D_800BCCC0_BD8C0.submode != 3) && ((s32) D_800BCCC0_BD8C0.submode < 4) && (func_8003F1D8_3FDD8() == 0) && (D_8014CCC0_14D8C0.external_a == 0) && (D_800BCCC0_BD8C0.local_gate == 0) && (D_8014CCC0_14D8C0.external_b == 0) && (D_800BCCC0_BD8C0.condition == 0)) {
            D_800BCCC0_BD8C0.pause_latch = 1U;
            D_800BCCC0_BD8C0.phase = 0;
            D_800BCCC0_BD8C0.phase_b = 0;
            func_80038BC8_397C8(3);
        }
    } else {
        func_8001FA80_20680();
    }
}
void func_8001FA3C_2063C(void) {
    func_80004240_4E40();
    func_80034EF8_35AF8(D_8006D328_6DF28);
    D_8015C5C8_15D1C8->unk_3addf = 1;
}
#pragma GLOBAL_ASM("asm/usa/nonmatchings/rotation_angles/func_8001FA80_20680.s")
