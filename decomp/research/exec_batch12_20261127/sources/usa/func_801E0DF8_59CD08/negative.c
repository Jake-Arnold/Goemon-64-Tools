#include "m2c_types.h"

typedef struct {
    u8 pad0[0x28];
    f32 unk28;
} Struct_1E0DF8;

extern f32 func_8001B5AC_1C1AC(Struct_1E0DF8 *);
void func_801DACDC_596BEC(s32, s32);
void func_801DD720_599630(s32, s32);

void func_801E0DF8_59CD08(s32 arg0, Struct_1E0DF8 *arg1) {
    func_801DD720_599630(arg0, 8);
    if ((((f32 (*)(Struct_1E0DF8 *))func_8001B5AC_1C1AC)(arg1) - 1.0f) <= arg1->unk28) {
        func_801DACDC_596BEC(arg0, 0xD1);
    }

    *(volatile int *)0x80000000 = 1;
}
