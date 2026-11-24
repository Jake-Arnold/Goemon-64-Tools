#include "common.h"
typedef struct {
    u8 pad0[0xADB6];
    u16 field_adb6;
    u8 pad1[0x1D];
    u8 field_add5;
    u8 field_add6;
    u8 pad2[0x41];
    u16 field_ae18;
    u8 pad3[0x203];
    u8 field_b01d;
} TransitionStatic;
extern TransitionStatic D_800BCCC0_BD8C0;
extern s32 D_800548D8_554D8;
extern s32 D_8006D328_6DF28;
extern u8 D_801CCB7C[];
extern void func_801CB460(void);
extern void func_80001C00_2800(s32, void *);
extern void func_8000383C_443C(void);
extern void func_80003880_4480(void);
extern void func_80034734_35334(void);
extern void func_8003488C_3548C(void *);
extern void func_80003728_4328(u8);
extern s32 func_80036908_37508(s32);
