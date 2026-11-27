#include "m2c_types.h"

typedef struct {
    u8 pad0[0x88];
    s32 unk88;
    s32 unk8C;
} UnkObj;

UnkObj *func_80034A78_35678(s32, s32, s32);
s32 func_801EDD04_5A9CD4(s32, u8);
void func_801F34C8_5AF498(UnkObj *, s32, u8);
extern s32 D_80209758_5C5728[];
extern u8 D_8021185C_5CD82C;

void func_801F80AC_5B407C(s32 arg0, u8 arg1) {
    UnkObj *temp_v0;

    if ((func_801EDD04_5A9CD4(arg0, arg1) == 0) && (D_8021185C_5CD82C == 0)) {
        temp_v0 = func_80034A78_35678(arg0, D_80209758_5C5728[arg1], 0);
        if (temp_v0 != NULL) {
            func_801F34C8_5AF498(temp_v0, arg0, arg1);
            temp_v0->unk88 = 0;
            temp_v0->unk8C = 0;
        }
    }
}
