#include "m2c_types.h"
extern M2C_UNK func_8003521C_35E1C;
extern M2C_UNK func_80038B98_39798;
extern M2C_UNK func_08000828_6C8A38;

typedef struct {
    u8 unk_00[0x8A];
    u16 unk_8A;
} Obj_080007CC;

void func_080007CC_6C89DC(Obj_080007CC *arg0, s32 arg1) {
    if (arg0->unk_8A++ >= 0xA) {
        arg0->unk_8A = 0;
        ((void (*)(s32))&func_80038B98_39798)(0x274);
        ((void (*)(void *))&func_8003521C_35E1C)(&func_08000828_6C8A38);
    }
}
