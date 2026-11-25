#include "jp_transition.h"
extern s32 D_80054B58_55758;
void func_8000B264_BE64(void);
void func_80020110_20D10(void);
void func_80003808_4408(void);
void func_80003870_4470(void);
void func_800028D8_34D8(void) {
    switch (g_system_ptr->unk_3add6) {
        case 0:
            func_80003760_4360();
            g_system_ptr->intended_room_id = 0x24C;
            func_8000B264_BE64();
            func_80020110_20D10();
            g_system.disable_graphics_tasks = 0;
            g_system_ptr->unk_3add6++;
            break;
        case 1:
            if (g_system.disable_graphics_tasks == 0 && (*(u16 *)((u8 *)g_system_ptr + 0x3B07C) | *(u16 *)((u8 *)g_system_ptr + 0x3B094)) & 0xD000) {
                g_system_ptr->stepw_end++;
            }
            func_80003808_4408();
            break;
        case 2:
            func_80003870_4470();
            break;
        case 3:
            if (D_80054B58_55758 == 0) {
                func_80003760_4360();
                g_system.disable_graphics_tasks = 0;
                g_system.unk_3ae18 &= 0x7FFF;
                func_8000364C_424C(5);
            }
            break;
    }
}
