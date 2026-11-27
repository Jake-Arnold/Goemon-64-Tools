#include "m2c_types.h"

typedef struct {
    u8 pad0[0x90];
    u8 unk90;
} Arg0;

typedef struct {
    u16 unk0;
    u8 pad2[0x16];
} UnkTbl;

void func_801DACDC_596BEC(Arg0 *, s32);
void func_801E7F50_5A3E60(Arg0 *);
s32 func_801F70B0_5B2FC0(Arg0 *, f32);
void func_801F7130_5B3040(Arg0 *);
void func_801F7140_5B3050(Arg0 *, f32);
extern UnkTbl D_800C7DB2[];

void func_801F6CC4_5B2BD4(Arg0 *arg0, s32 arg1) {
    func_801E7F50_5A3E60(arg0);
    func_801F7140_5B3050(arg0, 2.0f);
    if ((D_800C7DB2[arg0->unk90].unk0 & 0x4000) && (func_801F70B0_5B2FC0(arg0, 5.0f) != 0)) {
        func_801DACDC_596BEC(arg0, 0xB6);
    }
    if (func_801F70B0_5B2FC0(arg0, 1.0f) != 0) {
        func_801F7130_5B3040(arg0);
        func_801DACDC_596BEC(arg0, 0xB4);
    }
}
