#include "m2c_types.h"

extern void func_801DACDC_596BEC(void *, s32);
extern void func_801E1C90_59DBA0(void *);
extern void func_801E2264_59E174(void *);
extern void func_801E2344_59E254(void *);
extern void func_801E3358_59F268(void *);
extern void func_801E4624_5A0534(void *, s32);
extern s32 func_801E8390_5A42A0(void *);

typedef struct {
    u16 unk0;
    u8 pad[0x16];
} UnkDB4;

extern UnkDB4 D_800C7DB4[];

void func_801DF120_59B030(void *arg0, M2C_UNK arg1) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x5C);
    M2C_FIELD(temp_v0, u16 *, 0x30) = M2C_FIELD(temp_v0, u16 *, 0x30) + 1;
    func_801E1C90_59DBA0(arg0);
    if (M2C_FIELD(arg0, u16 *, 0x9A) != 0) {
        func_801E3358_59F268(arg0);
        func_801DACDC_596BEC(arg0, 0x3B);
        return;
    }
    if ((D_800C7DB4[M2C_FIELD(arg0, u8 *, 0x90)].unk0 & 0x4000) || (M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), u8 *, 0x68) == 3)) {
        func_801E4624_5A0534(arg0, 1);
        return;
    }
    if ((M2C_FIELD(arg0, u16 *, 0x98) != 0) && (func_801E8390_5A42A0(arg0) == 0)) {
        if (M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), u16 *, 0x30) < 0xF) {
            func_801E2264_59E174(arg0);
            func_801DACDC_596BEC(arg0, 0x1C);
            return;
        }
        func_801E2344_59E254(arg0);
        func_801DACDC_596BEC(arg0, 0x1B);
    }
}
