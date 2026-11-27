#include "m2c_types.h"
void func_8003521C_35E1C(void *);
extern M2C_UNK func_08000944_6EF2A4;

void func_080008EC_6EF24C(void *arg0, void *arg1) {
    void (*fn)(void *) = func_8003521C_35E1C;
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        M2C_FIELD(arg0, s32 *, 0x60) &= 0xFEFFFFFE;
        M2C_FIELD(arg0, s16 *, 0x8A) = 0xF;
        fn(&func_08000944_6EF2A4);
    }
}
