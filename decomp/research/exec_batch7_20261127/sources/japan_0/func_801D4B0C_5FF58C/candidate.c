#include "m2c_types.h"
typedef struct {
    u8 pad0[0x7C];
    s32 unk7C;
    u8 pad80[0x10];
    s32 unk90;
    s32 unk94;
} UnkObj_CEFB0;

UnkObj_CEFB0 *func_80034A78_35678(s32, void (*)(void), s32);
void func_801D4B60_5FF5E0(void);

UnkObj_CEFB0 *func_801D4B0C_5FF58C(s32 arg0, u8 arg1) {
    UnkObj_CEFB0 *temp_v0;

    temp_v0 = func_80034A78_35678(arg0, func_801D4B60_5FF5E0, 0);
    if (temp_v0 != NULL) {
        temp_v0->unk90 = arg0;
        temp_v0->unk94 = arg1;
        temp_v0->unk7C = 0xC;
    }
    return temp_v0;
}
