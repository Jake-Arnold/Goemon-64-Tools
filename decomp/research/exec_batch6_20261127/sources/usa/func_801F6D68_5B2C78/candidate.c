#include "m2c_types.h"

void func_801DACDC_596BEC(void *, s32);
void func_801E7F50_5A3E60(void *);
s32 func_801F70B0_5B2FC0(void *, f32);
void func_801F7140_5B3050(void *, f32);

typedef struct {
    u16 unk0;
    u8 pad[0x16];
} UnkDB2;

extern UnkDB2 D_800C7DB2[];

void func_801F6D68_5B2C78(void *arg0, s16 arg1) {
    func_801E7F50_5A3E60(arg0);
    func_801F7140_5B3050(arg0, 2.0f);
    if (D_800C7DB2[M2C_FIELD(arg0, u8 *, 0x90)].unk0 & 0x4000) {
        func_801DACDC_596BEC(arg0, 0xB2);
    }
    if (func_801F70B0_5B2FC0(arg0, 0.5f) != 0) {
        func_801DACDC_596BEC(arg0, 0xB5);
    }
}
