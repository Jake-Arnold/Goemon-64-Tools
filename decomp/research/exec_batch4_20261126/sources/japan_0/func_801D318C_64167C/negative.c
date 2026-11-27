#include "m2c_types.h"

typedef struct {
    u8 pad0[0x31C];
    s32 unk31C;
} Sub801CDA5C;

typedef struct {
    u8 pad0[0x64];
    f32 unk64;
    u8 pad68[0xEC - 0x68];
    Sub801CDA5C *unkEC;
} Struct801CDA5C;

f32 func_801D318C_64167C(Struct801CDA5C *arg0) {
    Sub801CDA5C *temp;
    f32 val;

    temp = arg0->unkEC;
    val = (f32) temp->unk31C / 1000.0f;
    { *(volatile s32 *)0x80000000 = 1; } return val - arg0->unk64;
}
