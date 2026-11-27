#include "m2c_types.h"
extern M2C_UNK func_80034E8C_35A8C;
extern M2C_UNK func_80038808_39408;
extern M2C_UNK func_080007D8_6CD458;

typedef struct {
    u8 unk_00[0x8A];
    u16 unk_8A;
} Obj_080007CC;

void func_0800077C_6CD3FC(Obj_080007CC *arg0, s32 arg1) {
    if (arg0->unk_8A++ >= 0xA) {
        arg0->unk_8A = 0;
        ((void (*)(s32))&func_80038808_39408)(0x274);
        ((void (*)(void *))&func_80034E8C_35A8C)(&func_080007D8_6CD458);
    }

    *(volatile s32 *)0x80000000 = 1;
}
