#ifndef GOEMON_SCRIPT_VM_H
#define GOEMON_SCRIPT_VM_H
#include "common.h"

typedef void (*VmTaskCallback)(void *, void *);
typedef struct { u8 unknown_00[0x10]; s32 countdown; } VmWork;
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
void func_8003E5EC_3F1EC(void);
void func_8003E620_3F220(void);

s32 func_8003DE48_3EA48(s32);

#ifdef GOEMON_DECOMP_HOST_TEST
#define VM_WORD_AT(address) (*(s32 *)(intptr_t)(address))
#define VM_U32_PTR(address) ((u32 *)(intptr_t)(address))
#else
#define VM_WORD_AT(address) (*(s32 *)(address))
#define VM_U32_PTR(address) ((u32 *)(address))
#endif
#endif
