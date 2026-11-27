#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern M2C_UNK func_08000BB8_6FBDB8;

typedef struct {
    u8 pad0[0x78];
    f32 unk78;
    u8 pad7C[4];
    f32 unk80;
    u8 pad84[6];
    s16 unk8A;
    u8 pad8C[0x44];
    s16 unkD0;
} Struct_08000C10;

void func_08000C10_6FBE10(Struct_08000C10 *arg0, M2C_UNK arg1) {
    arg0->unk80 = (f32) ((f64) (f32) arg0->unkD0 / 10.0);
    arg0->unk8A = 0x28;
    arg0->unk78 = 0.5f;
    ((void (*)(M2C_UNK *))func_8003521C_35E1C)(&func_08000BB8_6FBDB8);

    *(volatile int *)0x80000000 = 1;
}
