#include "jp_transition.h"
extern u16 D_80161FFC_162BFC;
void func_80002A58_3658(void) {
    u8 i;
    s32 state = g_system_ptr->unk_3add6;
    switch (state) {
        case 0:
            func_80003760_4360();
            func_80001BA0_27A0(15, (void *)func_801D0B90);
            i = 0xFF;
            while (1) {
                if (i == 0) break;
                i--;
            }
            g_system_ptr->unk_3add6++;
            return;
        case 1:
            g_system_ptr->intended_room_group_index = 0;
            func_800344FC_350FC(D_801D228C);
            g_system_ptr->unk_3add6++;
            return;
        case 2:
            func_800343A4_34FA4();
            if (g_system.stepw_end != 0) {
                func_80038838_39438(7);
                g_system_ptr->unk_3add6++;
            }
            return;
        case 3:
            if (g_system.stepw_end != 0) {
                func_80003760_4360();
                if (g_system.stepw_end == 1) {
                    g_system.unk_3ae18 = 0x8000;
                    func_8000364C_424C(5);
                }
                if (g_system.stepw_end == 2) {
                    if (D_80161FFC_162BFC == 0x1D1) {
                        func_8000364C_424C(9);
                    } else {
                        func_8000364C_424C(11);
                    }
                }
            }
            return;
    }
}
