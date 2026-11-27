#include "m2c_types.h"

typedef struct {
    u8 pad0[0x28];
    f32 unk28;
} Struct_1E0DF8;

extern f32 func_8001B13C_1BD3C(Struct_1E0DF8 *);
void func_801E019C_59C16C(s32, s32);
void func_801E2AD0_59EAA0(s32, s32);

void func_801E6010_5A1FE0(s32 arg0, Struct_1E0DF8 *arg1) {
    func_801E2AD0_59EAA0(arg0, 8);
    if ((((f32 (*)(Struct_1E0DF8 *))func_8001B13C_1BD3C)(arg1) - 1.0f) <= arg1->unk28) {
        func_801E019C_59C16C(arg0, 0xD1);
    }
}
