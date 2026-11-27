#include "m2c_types.h"

typedef struct {
    u8 pad0[0x88];
    s32 unk88;
    s32 unk8C;
} UnkObj;

UnkObj *func_80034E08_35A08(s32, s32, s32);
s32 func_801E8C44_5A4B54(s32, u8);
void func_801EE4AC_5AA3BC(UnkObj *, s32, u8);
extern s32 D_80204868_5C0778[];
extern u8 D_8020CA6C_5C897C;

void func_801F309C_5AEFAC(s32 arg0, u8 arg1) {
    UnkObj *temp_v0;

    if ((func_801E8C44_5A4B54(arg0, arg1) == 0) && (D_8020CA6C_5C897C == 0)) {
        temp_v0 = func_80034E08_35A08(arg0, D_80204868_5C0778[arg1], 0);
        if (temp_v0 != NULL) {
            func_801EE4AC_5AA3BC(temp_v0, arg0, arg1);
            temp_v0->unk88 = 0;
            temp_v0->unk8C = 0;
        }
    }

    *(volatile s32 *)0x80000000 = 1;
}
