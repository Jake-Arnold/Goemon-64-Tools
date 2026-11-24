#include "jp_transition.h"
void func_80003090_3C90(u8 state) {
    state = g_system_ptr->unk_3add6;
    switch (state) {
        case 0:
            func_80003760_4360();
            func_80001BA0_27A0(15, (void *)func_801D0B90);
            state = 0xFF;
            while (1) {
                if (state == 0) break;
                state--;
            }
            g_system_ptr->unk_3add6++;
            return;
        case 1:
            g_system_ptr->intended_room_group_index = 3;
            func_800344FC_350FC(D_801D228C);
            g_system_ptr->unk_3add6++;
            return;
        case 2:
            state = g_system.stepw_end;
            switch (state) {
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
