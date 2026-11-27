#include "m2c_types.h"

typedef struct {
    u8 pad0[0xE8];
    f32 unkE8;
} Arg0_1DF5A4;

typedef struct {
    u8 pad0[0x28];
    f32 unk28;
} Arg1_1DF5A4;

extern u8 func_8001B5AC_1C1AC[];
void func_801DACDC_596BEC(Arg0_1DF5A4 *, s32);
void func_801E307C_59EF8C(Arg0_1DF5A4 *);

void func_801DF5A4_59B4B4(Arg0_1DF5A4 *arg0, Arg1_1DF5A4 *arg1) {
    arg0->unkE8 = 0.0f;
    func_801E307C_59EF8C(arg0);
    if ((((f32 (*)(Arg1_1DF5A4 *))func_8001B5AC_1C1AC)(arg1) - 1.0f) <= arg1->unk28) {
        func_801DACDC_596BEC(arg0, 0);
    }
}
