#include "jp_transition.h"
extern s32 D_80054B58_55758;
void func_8000B1E4_BDE4(void);
typedef struct { u8 pad0[0xADB6]; s16 field_adb6; u8 pad1[0x1E]; u8 field_add6; } TransitionStatic;
#define TS (*(TransitionStatic *)((u8 *)&g_system + 0x30000))
void func_80002E10_3A10(void) {
    u8 *p = (u8 *)&g_system + 0x30000;
    u8 state = p[0xADD6];
    if (state == 0 && (*(s16 *)(p + 0xADB6)) == 0) {
        (*(s16 *)(p + 0xADB6)) = 1;
        p[0xADD6] = state + 1;
    } else if (D_80054B58_55758 == 0) {
        func_8000B1E4_BDE4();
        p[0xADD6] = 1;
        func_80003760_4360();
        func_8000364C_424C(13);
    }
}
