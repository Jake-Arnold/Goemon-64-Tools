#include "jp_transition.h"
extern s32 D_80054B58_55758;
void func_801D0DF0(void);
void func_80036624_37224(s32);
s32 func_800364B0_370B0(s32);
void func_80003808_4408(void);
void func_80003870_4470(void);
void func_800024B8_30B8(void) {
    u16 i;
    switch (g_system.unk_3add6) {
        case 0:
            g_system_ptr->retraces_per_game_step = 1;
            func_80001BA0_27A0(20, (void *)func_801D0B90);
            i = 0x7FFF;
            if (i != 0) {
                do { i--; } while (i != 0);
            }
            g_system_ptr->unk_3add6++;
            break;
        case 1:
            func_80003760_4360();
            func_801D0DF0();
            g_system_ptr->retraces_per_game_step = 0;
            func_80036624_37224(D_80072E08_73A08);
            g_system_ptr->unk_3add6++;
            break;
        case 2:
            g_system_ptr->retraces_per_game_step = 0;
            func_800343A4_34FA4();
            if (func_800364B0_370B0(D_80072E08_73A08) == 0) {
                g_system_ptr->unk_3add6++;
            }
            break;
        case 3:
            if ((g_system_ptr->controller[0].button_pressed | g_system_ptr->controller[1].button_pressed) & 0xD000) {
                g_system.stepw_end = 2;
            }
            func_80003808_4408();
            break;
        case 4:
            func_80003870_4470();
            break;
        case 5:
            if (D_80054B58_55758 == 0) {
                g_system.disable_graphics_tasks = 0;
                func_80003760_4360();
                if (g_system.stepw_end == 1) {
                    func_8000364C_424C(6);
                } else {
                    func_8000364C_424C(5);
                }
            }
            break;
    }
}
