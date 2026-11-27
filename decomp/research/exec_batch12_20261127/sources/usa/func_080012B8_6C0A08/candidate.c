#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern u8 func_80038B98_39798[];
extern u8 func_8021BB04_5D6FD4[];
extern u8 func_08001324_6C0A74[];

void func_080012B8_6C0A08(void *arg0, s32 arg1) {
    if (((s32 (*)(void *, u32, u32, u32))func_8021BB04_5D6FD4)(arg0, 0xC3520000, 0x41B00000, 0x3F000000) == 0) {
        ((void (*)(s32))func_80038B98_39798)(0x155);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x14;
        ((void (*)(void *))func_8003521C_35E1C)(func_08001324_6C0A74);
    }
}
