#include "jp_transition.h"
void func_80003090_3C90(void) {
    u8 i;
    switch (g_system_ptr->unk_3add6) {
        case 0:
            func_80003760_4360();
            func_80001BA0_27A0(15, (void *)func_801D0B90);
            i = 0xFF;
            goto test_countdown;
            decrement_countdown:
            i--;
            test_countdown:
            if (i != 0) goto decrement_countdown;
            g_system_ptr->unk_3add6++;
            break;
        case 1:
            g_system_ptr->intended_room_group_index = 3;
            func_800344FC_350FC(D_801D228C);
            g_system_ptr->unk_3add6++;
            break;
        case 2:
            switch (g_system.stepw_end) {
                case 1:
                    func_80003760_4360();
                    g_system_ptr->intended_room_group_index = 3;
                    g_system.stepw_end = 0;
                    func_800344FC_350FC(D_801D228C);
                    break;
                case 2:
                    func_80003760_4360();
                    g_system_ptr->intended_room_group_index = 1;
                    g_system.stepw_end = 0;
                    func_800344FC_350FC(D_801D228C);
                    break;
                case 3:
                    func_80003760_4360();
                    g_system.unk_3ae18 = 0x8000;
                    func_8000364C_424C(5);
                    break;
                case 0:
                    func_800343A4_34FA4();
                    break;
            }
            break;
    }
}
