#ifndef GOEMON_SCRIPT_VM_H
#define GOEMON_SCRIPT_VM_H
#include "common.h"

extern s32 D_80077858_78458;
extern s32 D_8007785C_7845C;
extern s32 D_801C7770_1C8370;
extern s32 D_801C7774_1C8374;
extern u16 D_801C790C_1C850C;
extern u8 *D_801FC604_5B8514;
extern u8 *D_801FC608;
void func_8003E680_3F280(void);
extern s32 D_801C7740_1C8340;
extern u16 D_801C7742_1C8342;
extern s32 D_801C7744_1C8344;
extern u8 D_801C7747_1C8347;
extern u8 D_801C774B_1C834B;
extern u32 D_801C7750_1C8350;
extern s32 D_801C78E8_1C84E8;
extern u16 D_801C78EA_1C84EA;
s32 func_800141C4_14DC4(u32);
s32 func_80013B14_14714(s32);
s32 func_80001E50_2A50(u32);
void func_80034EF8_35AF8(s32);
void func_80038BC8_397C8(u16);
void func_80038C30_39830(u16, u8, u8);
void func_80038B98_39798(u16);
void func_80037C9C_3889C(s32, s32);
void func_80037C20_38820(s32, s32, s32);

/* Only accessed window fields are characterized; names remain provisional. */
typedef struct {
    u8 unknown00[0x32];
    s16 field32, field34;
    u8 unknown36[8];
    s16 field3e, field40, field42;
    u8 unknown44[12];
    s32 field50, field54;
} VmWindow;
typedef struct { s32 x, y; u32 texture, pattern; } VmPrompt;
extern VmWindow *D_80167C48_168848[];
extern VmPrompt D_801C78D8_1C84D8;
extern u8 D_80077150_77D50[];

typedef void (*VmTaskCallback)(void *, void *);
typedef struct { u8 unknown00[0xD4]; u32 flags; } VmControl;
typedef struct { u8 unknown00[0xBC]; u32 resume; } VmWaitOwner;
extern VmControl D_8015CC30_15D830;
extern s32 D_801C78F4_1C84F4, D_801C78F8_1C84F8;
extern s32 D_801C77FC_1C83FC;
void func_8003F18C_3FD8C(void *, void *);
typedef struct {
    u8 unknown_00[4];
    u16 last_direction, repeat_ticks;
    s16 marker;
    u8 unknown_0a[2];
    s32 choice_state, countdown;
} VmWork;
typedef struct { s32 x, y; u32 previous, next, script; } VmChoice;
typedef CONTROLLER_W VmInput;
extern VmChoice *D_801C7800_1C8400;
extern VmChoice D_801C7808_1C8408[];
extern VmInput D_801C7908_1C8508;
extern VmTaskCallback D_801C78D0_1C84D0;
s32 func_8003E888_3F488(VmChoice *);
void func_8003E9E8_3F5E8(VmChoice *);
s32 func_8003EA14_3F614(void);
s32 func_8003EACC_3F6CC(VmChoice *);
s32 func_800240DC_24CDC(s32);
void func_8000D060_DC60(s32, s16);
s16 *func_8003DF98_3EB98(s32, s16 *);
extern u16 *D_80077550_78150[];
extern u16 D_8007CCA4_7D8A4[];
extern void *D_80077860_78460;
extern s32 D_801C7754_1C8354;
extern s32 D_801C7758_1C8358;
extern s32 D_801C775C_1C835C;
extern s32 D_801C7760_1C8360;
extern s32 D_801C7764_1C8364;
extern s32 D_801C7768_1C8368;
extern s32 D_801C776C_1C836C;
extern s32 D_801C77A0_1C83A0;
extern s32 D_801C77E0_1C83E0;
extern VmWork D_801C77E8_1C83E8;
extern s32 D_801C78EC_1C84EC;
extern s32 D_801C78F0_1C84F0;
extern s8 D_801C78FC_1C84FC;
extern u8 D_801C7930_1C8530;

void func_8000C260_CE60(s32, s32, s32, s32, s32, s32, s32);
s32 func_8000C314_CF14(s32);
void func_8000C3A0_CFA0(s32);
void func_8000C838_D438(void);
void func_80034B24_35724(VmTaskCallback, s32);
void func_80035044_35C44(void *);
void func_8003521C_35E1C(VmTaskCallback);
void func_8003D0B0_3DCB0(void);
void func_8003D468_3E068(s32, s32);
s32 func_8003D68C_3E28C(void);
void func_8003CFD0_3DBD0(void *, void *);
void func_8003D01C_3DC1C(void *, void *);
void func_8003D428_3E028(void);
extern s32 D_801C7900_1C8500, D_801C7904_1C8504;
extern s32 D_800779A0_785A0[];
extern s16 D_80078608_79208[];
extern u8 *D_801FC600_5B8510[];
s32 func_8003F1D8_3FDD8(void);
void func_8003E5EC_3F1EC(void);
void func_8003E620_3F220(void);

s32 func_8003DE48_3EA48(s32);

#ifdef GOEMON_DECOMP_HOST_TEST
#define VM_WORD_AT(address) (*(s32 *)(intptr_t)(address))
#define VM_U32_ADDRESS(pointer) ((u32)(uintptr_t)(pointer))
#define VM_CALLBACK(address) ((VmTaskCallback)(uintptr_t)(u32)(address))
#define VM_U32_PTR(address) ((u32 *)(intptr_t)(address))
#else
#define VM_WORD_AT(address) (*(s32 *)(address))
#define VM_U32_ADDRESS(pointer) ((u32)(pointer))
#define VM_CALLBACK(address) ((VmTaskCallback)(address))
#define VM_U32_PTR(address) ((u32 *)(address))
#endif
#endif
