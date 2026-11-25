#include "jp_transition.h"
s32 func_801D6DC0(void);
void func_8000230C_2F0C(void) {
    u16 i;
    switch (g_system_ptr->unk_3add6) {
        case 0:
            func_80001BA0_27A0(15, (void *)func_801D0B90);
            i = 0xFFFF;
            while (1) {
                if (i == 0) break;
                i--;
            }
            g_system.disable_graphics_tasks = i & 0xFFFF;
        case 1:
            g_system.unk_3add6++;
            break;
        case 2:
            if (func_801D6DC0()) {
                g_system.disable_graphics_tasks = 1;
                g_system.unk_3add6++;
            }
            break;
        case 3:
            func_8000364C_424C(3);
            break;
    }
}
