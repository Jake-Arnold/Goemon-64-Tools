#include "m2c_types.h"

typedef struct {
    u16 unk0;
    u8 pad[0x16];
} UnkStruct18;

void func_801DACDC_596BEC(void *, s32);
void func_801E20A0_59DFB0(void *);
extern UnkStruct18 D_800C7DB4[];

s32 func_801DF8B8_59B7C8(void *arg0) {
    void *temp_v0;

    if (D_800C7DB4[M2C_FIELD(arg0, u8 *, 0x90)].unk0 & 0x8000) {
        temp_v0 = M2C_FIELD(arg0, void **, 0x5C);
        if ((M2C_FIELD(temp_v0, u8 *, 0x59) & 0x80) && !(M2C_FIELD(temp_v0, u8 *, 0x18) & 1)) {
            M2C_FIELD(temp_v0, f32 *, 0x50) = 0.0f;
            M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 0) = 0;
            func_801E20A0_59DFB0(arg0);
            func_801DACDC_596BEC(arg0, 0x17);
            return 1;
        }
    }
    return 0;
}
