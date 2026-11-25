#include "jp_transition.h"
void func_80003090_3C90(s32 state) {
    u8 i;
    state = g_system_ptr->unk_3add6;
    switch (state) {
        case 0:
            func_80003760_4360();
            func_80001BA0_27A0(15, (void *)func_801D0B90);
            i = 0xFF;
            while (1) {
                if (i == 0) break;
                i--;
            }
            g_system_ptr->unk_3add6 = ((i = g_system_ptr->unk_3add6) & 0xFF) + 1;
            return;
        case 1:
            g_system_ptr->intended_room_group_index = 3;
            func_800344FC_350FC(D_801D228C);
            g_system_ptr->unk_3add6++;
            return;
        case 2:
            switch (g_system.stepw_end) {
                case 1:
                    func_80003760_4360();
                    g_system_ptr->intended_room_group_index = 3;
                    g_system.stepw_end = 0;
                    func_800344FC_350FC(D_801D228C);
                    return;
                case 2:
                    func_80003760_4360();
                    g_system_ptr->intended_room_group_index = 1;
                    g_system.stepw_end = 0;
                    func_800344FC_350FC(D_801D228C);
                    return;
                case 3:
                    func_80003760_4360();
                    g_system.unk_3ae18 = 0x8000;
                    func_8000364C_424C(5);
                    return;
                case 0:
                    func_800343A4_34FA4();
                    return;
            }
            return;
    }
}
