#include "m2c_types.h"
extern M2C_UNK func_80034E8C_35A8C;
extern M2C_UNK func_80038808_39408;
extern M2C_UNK func_801E2188_59E158;
extern M2C_UNK func_802198E4_5D4E74;

typedef struct {
    u8 unk_00[0x68];
    s32 unk_68;
} Obj_80214AEC;

void func_80219884_5D4E14(Obj_80214AEC *arg0, s32 arg1) {
    if (arg0->unk_68 & 0x200) {
        ((void (*)(s32))&func_80038808_39408)(0x26C);
        ((void (*)(s32))&func_801E2188_59E158)(2);
        ((void (*)(void *))&func_80034E8C_35A8C)(&func_802198E4_5D4E74);
    }
}
