#include "jp_transition.h"
extern s32 D_80054B58_55758;
void func_8000B120_BD20(void);
void func_80002D84_3984(void) {
    u8 state = g_system.unk_3add6;
    if (state == 0 && (*(s16 *)((u8 *)&g_system + 0x3ADB6)) == 0) {
        (*(s16 *)((u8 *)&g_system + 0x3ADB6)) = 1;
        g_system.unk_3add6 = state + 1;
    } else if (D_80054B58_55758 == 0) {
        func_8000B120_BD20();
        g_system.unk_3add6 = 1;
        func_80003760_4360();
        func_8000364C_424C(13);
    }
}
