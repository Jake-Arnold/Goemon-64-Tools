#include "jp_transition.h"
extern Gfx *g_display_list_head_ptr;
extern u8 D_80162408_163008[3][4];
void func_80004170_4D70(void);
void func_800134D0_140D0(void);
s32 func_801D1184(void);
void func_800036B0_42B0(void);
void func_8000359C_419C(void);
s32 func_80013D54_14954(s32);
s32 func_801D132C(Gfx **, s32);
s32 func_80022EB0_23AB0(void);
s32 func_80022FC0_23BC0(void);
s32 func_800230E4_23CE4(void);
s32 func_80023154_23D54(void);
s32 func_80023234_23E34(void *);
void func_800020D8_2CD8(void) {
    u16 i;
    s32 j;
    u8 *p;
    switch (g_system_ptr->unk_3add6) {
        case 0:
            func_80001BA0_27A0(23, (void *)func_801D0B90);
            i = 0xFFFF;
            while (1) {
                if (i == 0) break;
                i--;
            }
            g_system.unk_3add6++;
            break;
        case 1:
            func_80004170_4D70();
            func_800134D0_140D0();
            if ((g_system_ptr->controller[0].button_held_down & 0x1000) && g_system.is_controller_pak_connected == 0) {
                if (func_801D1184()) {
                    func_800036B0_42B0();
                } else {
                    func_8000359C_419C();
                }
            } else {
                func_800036B0_42B0();
            }
            break;
        case 2:
            g_system.dont_process_draw_lists = 1;
            if (func_801D132C(&g_display_list_head_ptr, func_80013D54_14954(2))) {
                func_8000359C_419C();
            }
            break;
        case 3:
            g_system.disable_graphics_tasks = 1;
            g_system.dont_process_draw_lists = 0;
            g_system.is_controller_pak_connected = func_80022EB0_23AB0();
            if (g_system.is_controller_pak_connected != 0 || func_80022FC0_23BC0() || func_800230E4_23CE4() || func_80023154_23D54() || func_80023234_23E34(D_80162408_163008)) {
                j = 0;
                p = &D_80162408_163008[0][0];
                do {
                    j += 4;
                    p[0] = 0;
                    p[1] = 0;
                    p[2] = 0;
                    p[3] = 0;
                    p += 4;
                } while (j != 12);
            }
            i = 0xFFFF;
            while (1) {
                if (i == 0) break;
                i--;
            }
            func_8000359C_419C();
            break;
        case 4:
            func_800036B0_42B0();
            break;
    }
}
