#include "jp_transition.h"
extern Gfx *g_display_list_head_ptr;
Gfx *func_801D0D98(s16, Gfx *);
void func_800023F4_2FF4(s32 state) {
    u16 i;
    state = g_system_ptr->unk_3add6;
    if (state == 0) {
        func_80001BA0_27A0(22, (void *)func_801D0B90);
        i = 0xFFFF;
        while (1) {
            if (i == 0) break;
            i--;
        }
        g_system.disable_graphics_tasks = 0;
    }
    func_801D0B90();
    g_display_list_head_ptr = func_801D0D98(g_system.current_graphics_pool, g_display_list_head_ptr);
    if (g_system_ptr->stepw != 3) {
        g_system_ptr->retraces_per_game_step = 2;
        osViSetSpecialFeatures(0x5A);
    }
    g_system.unk_3ae18 = 0x8000;
}
