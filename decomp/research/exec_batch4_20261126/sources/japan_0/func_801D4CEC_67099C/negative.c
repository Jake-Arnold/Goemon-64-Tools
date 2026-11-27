#include "m2c_types.h"

typedef struct {
    u8 pad0[0x28];
    f32 unk28;
} Sub801CF5BC;

typedef struct {
    u8 pad0[0x18];
    Sub801CF5BC *unk18;
} Struct801CF5BC;

s32 func_801D4CEC_67099C(Struct801CF5BC *arg0, s16 arg1, s16 arg2) {
    Sub801CF5BC *temp_v1;

    temp_v1 = arg0->unk18;
    temp_v1->unk28 += (f32) arg2 / 1000.0f;
    if (temp_v1->unk28 >= (f32) arg1) {
        temp_v1->unk28 -= (f32) arg1;
        { *(volatile s32 *)0x80000000 = 1; } return 1;
    }
    return 0;
}
