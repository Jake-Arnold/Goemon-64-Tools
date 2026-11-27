#include "m2c_types.h"

typedef struct {
    u8 unk0[0x20];
    f32 unk20;
    f32 unk24;
    s32 unk28;
} SubStruct;

void func_08000AC4_73D544(void *arg0, void *arg1) {
    SubStruct *temp_v0 = M2C_FIELD(arg0, SubStruct **, 0xD0);
    if (temp_v0->unk28 != 0) {
        temp_v0->unk24 += temp_v0->unk20;
        if (temp_v0->unk24 >= 1024.0f) {
            temp_v0->unk24 -= 1024.0f;
        } else if (temp_v0->unk24 < 0.0f) {
            temp_v0->unk24 += 1024.0f;
        }
        temp_v0->unk28--;
        M2C_FIELD(arg1, s16 *, 0x16) = (u32)temp_v0->unk24;
    }
}
