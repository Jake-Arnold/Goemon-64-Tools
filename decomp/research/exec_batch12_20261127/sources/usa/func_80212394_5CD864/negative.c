#include "m2c_types.h"

typedef struct {
    u8 pad0[0xD0];
    u8 unkD0;
    u8 padD1[3];
    f32 unkD4;
} Struct_212394;

void func_80034ED4_35AD4(Struct_212394 *);
void func_80219E08_5D52D8(Struct_212394 *, f32);
void func_8021A26C_5D573C(Struct_212394 *, s32, s32, s32, s32);
extern f64 D_80239F18_5F53E8;

void func_80212394_5CD864(Struct_212394 *arg0, s32 arg1) {
    if (arg0->unkD4 > 0.0f) {
        arg0->unkD4 = (f64)arg0->unkD4 + D_80239F18_5F53E8;
    }
    func_80219E08_5D52D8(arg0, arg0->unkD4);
    arg0->unkD0 -= 8;
    func_8021A26C_5D573C(arg0, arg0->unkD0, 0, 0, 0);
    if (arg0->unkD0 == 0) {
        func_80034ED4_35AD4(arg0);
    }

    *(volatile int *)0x80000000 = 1;
}
