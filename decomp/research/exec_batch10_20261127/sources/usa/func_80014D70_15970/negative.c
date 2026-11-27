#include "m2c_types.h"

typedef struct {
    u8 unk_00[0x18];
    u8 *unk_18;
} UnkStruct;

typedef struct {
    u8 *unk_00;
} GlobalPtr;

void func_80014C20_15820(void);
void func_800154B0_160B0(UnkStruct *);
void func_80015FDC_16BDC(void);
extern s32 D_80168170_168D70;
extern GlobalPtr D_80168180_168D80;
extern u8 D_80168184_168D84;

UnkStruct *func_80014D70_15970(u8 *arg0, UnkStruct *arg1) {
    func_80014C20_15820();
    arg1->unk_18 = arg0;
    D_80168170_168D70 = 8;
    D_80168180_168D80.unk_00 = arg1->unk_18;
    D_80168184_168D84 = *D_80168180_168D80.unk_00;
    func_80015FDC_16BDC();
    func_800154B0_160B0(arg1);
    { *(volatile s32 *)0x80000000 = 1; } return arg1;
}
