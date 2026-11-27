#include "m2c_types.h"

typedef struct {
    u8 pad0[0x60];
    s32 unk60;
    u8 pad64[0x26];
    u16 unk8A;
} Unk04E8_0;

typedef struct {
    u8 pad0[0x16];
    u16 unk16;
} Unk04E8_1;

extern u8 func_8003521C_35E1C[];
extern u8 func_8021B424_5D68F4[];
extern u8 func_08000558_6ACAA8[];

void func_080004E8_6ACA38(Unk04E8_0 *arg0, Unk04E8_1 *arg1) {
    arg1->unk16 += 8;
    arg0->unk8A--;
    if (arg0->unk8A == 0) {
        arg0->unk8A = 0x32;
        arg0->unk60 = 0x261;
        ((void (*)(Unk04E8_0 *, u16, s32))func_8021B424_5D68F4)(arg0, arg1->unk16, 0x3F800000);
        ((void (*)(u8 *))func_8003521C_35E1C)(func_08000558_6ACAA8);
    }
}
