#include "m2c_types.h"
s32 func_801E0954_59C924(void *, s32, M2C_UNK, M2C_UNK, f32); /* extern */
M2C_UNK func_801E2BE0_59EBB0(void *, M2C_UNK);              /* extern */
extern s32 D_801624B0_1630B0;

void func_801E7CE8_5A3CB8(void *arg0) {
    void *temp_v1;

    func_801E2BE0_59EBB0(arg0,4);
    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s32 *, 0x88) = func_801E0954_59C924(arg0, D_801624B0_1630B0, 0x196, 0x80, 115.0f);
    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 0x34) = 0;
    temp_v1 = M2C_FIELD(arg0, void **, 0x5C);
    if (M2C_FIELD(temp_v1, s32 *, 0x88) != 0) {
        M2C_FIELD(arg0, f32 *, 0xE4) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0xE8) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x68) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x6C) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x70) = 0.0f;
        return;
    }
    M2C_FIELD(arg0, f32 *, 0xE4) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0xE8) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x70) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x6C) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x68) = 0.0f;
    M2C_FIELD(temp_v1, s8 *, 0x2C) = 0;
    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 0x30) = 0;
}
