#include "m2c_types.h"
typedef struct {
    u8 pad0[0x7C];
    s32 unk7C;
    u8 pad80[0x10];
    s32 unk90;
    s32 unk94;
} UnkObj_CEFB0;

UnkObj_CEFB0 *func_80034E08_35A08(s32, void (*)(void), s32);
void func_801CF004_5FA3E4(void);

UnkObj_CEFB0 *func_801CEFB0_5FA390(s32 arg0, u8 arg1) {
    UnkObj_CEFB0 *temp_v0;

    temp_v0 = func_80034E08_35A08(arg0, func_801CF004_5FA3E4, 0);
    if (temp_v0 != NULL) {
        temp_v0->unk90 = arg0;
        temp_v0->unk94 = arg1;
        temp_v0->unk7C = 0xC;
    }
    { *(volatile s32 *)0x80000000 = 1; } return temp_v0;
}
