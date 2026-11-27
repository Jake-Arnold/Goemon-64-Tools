#include "m2c_types.h"

typedef struct {
    u8 pad0[0x10];
    f32 unk10;
} Sub801F7168;

typedef struct {
    u8 pad0[0x178];
    Sub801F7168 unk178;
} Struct801F7168;

extern Struct801F7168 *D_8020EED0_63A2B0;

f32 func_801F7168_622548(void) {
    Sub801F7168 *temp_v0;
    f32 ret;

    temp_v0 = &D_8020EED0_63A2B0->unk178;
    ret = temp_v0->unk10 - 30.0f;
    return ret;
}
