#include "default_entrance.h"
#pragma GLOBAL_ASM("asm/usa/nonmatchings/default_entrance/func_80020F10_21B10.s")
extern s32 D_8006CFBC_6DBBC, D_8006CFB8_6DBB8, D_8015C5DC_15D1DC;
void func_8000B864_C464(void);
void func_80003728_4328(u8);
void func_80021444_22044(void) {
    if (D_8006CFBC_6DBBC != 0xFF) {
        D_8015C5C8_15D1C8->unk_cf8a0 = 1;
        D_8015C608_15D208.half_204 = D_8015C5C8_15D1C8->intended_room_id;
        D_8015C608_15D208.byte_206 = D_8015C5C8_15D1C8->intended_room_group;
        D_8015C5DC_15D1DC = D_8006CFB8_6DBB8;
        func_800214E4_220E4();
        func_8000B864_C464();
        func_80003728_4328(0x0B);
        return;
    }
    func_80003728_4328(0x0B);
}
void func_800214E4_220E4(void) { if (D_8006B780_6C380[D_8015C5C8_15D1C8->intended_room_id].x != 0 || D_8006B780_6C380[D_8015C5C8_15D1C8->intended_room_id].y != 0 || D_8006B780_6C380[D_8015C5C8_15D1C8->intended_room_id].z != 0) { D_8015C608_15D208.half_20A=D_8006B780_6C380[D_8015C5C8_15D1C8->intended_room_id].x; D_8015C608_15D208.half_20C=D_8006B780_6C380[D_8015C5C8_15D1C8->intended_room_id].y; D_8015C608_15D208.half_20E=D_8006B780_6C380[D_8015C5C8_15D1C8->intended_room_id].z; D_8015C608_15D208.half_210=D_8006B780_6C380[D_8015C5C8_15D1C8->intended_room_id].heading; D_8015C608_15D208.half_208=D_8006B780_6C380[D_8015C5C8_15D1C8->intended_room_id].mode; } else { D_8015C608_15D208.half_20A=0; D_8015C608_15D208.half_20C=0; D_8015C608_15D208.half_20E=0; D_8015C608_15D208.half_210=0; D_8015C608_15D208.half_208=0; } }
