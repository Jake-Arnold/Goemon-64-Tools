#include "jp_transition.h"
extern u8 D_80212090[];
void func_80004840_5440(void);
void func_80003808_4408(void);
void func_80003870_4470(void);
void func_800026B8_32B8(void) {
    u8 i;
    u8 state = g_system_ptr->unk_3add6;
    switch (state) {
        case 0:
            func_80003760_4360();
            func_80004840_5440();
            if (g_system_ptr->unk_3add6 == 0) {
                func_80001BA0_27A0(11, (void *)func_801D0B90);
                func_80001BA0_27A0(19, D_80212090);
                i = 0xFF;
                while (1) {
                    if (i == 0) break;
                    i--;
                }
            }
            state = g_system_ptr->unk_3add6;
        case 1:
            g_system_ptr->unk_3add6 = state + 1;
            break;
        case 2:
            g_system_ptr->retraces_per_game_step = 2;
            g_system.unk_3ae16 = 0;
            g_system.disable_graphics_tasks = 0;
            func_800344FC_350FC(D_80212090);
            g_system_ptr->unk_3add6++;
            break;
        case 3:
            func_80003808_4408();
            break;
        case 4:
            func_80003870_4470();
            break;
        case 5:
            g_system_ptr->unk_3b01d--;
            if (g_system_ptr->unk_3b01d == 0) {
                g_system.disable_graphics_tasks = 0;
                func_80003760_4360();
                if (g_system.stepw_end == 1) {
                    if (g_system.unk_3ae18 & 0x8000) {
                        func_8000364C_424C(6);
                    } else {
                        g_system.unk_3adda = 0;
                        func_8000364C_424C(7);
                    }
                }
                if (g_system.stepw_end == 2) {
                    func_8000364C_424C(8);
                }
                if (g_system.stepw_end == 3) {
                    func_8000364C_424C(15);
                }
            }
            break;
    }
}
