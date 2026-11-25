#include "jp_transition.h"
extern s32 D_80054B58_55758;
void func_80020110_20D10(void);
void func_80036624_37224(s32);
s32 func_800364B0_370B0(s32);
void func_80003808_4408(void);
void func_80003870_4470(void);
void func_8000B550_C150(void);
void func_80002EF4_3AF4(void) {
    u8 state;
    switch (g_system_ptr->unk_3add6) {
        case 0:
            g_system.disable_graphics_tasks = 1;
            g_system.unk_3add6++;
            break;
        case 1:
            if (D_80054B58_55758 == 0) {
                func_80003760_4360();
                g_system_ptr->intended_room_group = 12;
                g_system_ptr->intended_room_group_index = 0;
                func_80020110_20D10();
                func_80036624_37224(D_80072E08_73A08);
                state = g_system_ptr->unk_3add6;
                g_system_ptr->unk_3add6 = state + 1;
            }
            break;
        case 2:
            g_system.disable_graphics_tasks = 0;
            func_800364B0_370B0(D_80072E08_73A08);
            func_80003808_4408();
            break;
        case 3:
            func_80003870_4470();
            break;
        case 4:
            if (D_80054B58_55758 == 0) {
                func_80003760_4360();
                if (g_system.stepw_end == 1) {
                    func_8000B550_C150();
                    g_system.unk_3ae0c++;
                    func_8000364C_424C(11);
                } else {
                    func_8000364C_424C(3);
                }
            }
            break;
    }
}
