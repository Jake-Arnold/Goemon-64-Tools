#include "jp_transition.h"
extern s32 D_80054B58_55758;
void func_8000B120_BD20(void);
typedef struct { u8 pad0[0xADB6]; s16 field_adb6; u8 pad1[0x1E]; u8 field_add6; } TransitionStatic;
extern TransitionStatic D_800C24B0;
#define TS D_800C24B0
void func_80002D84_3984(u8 state) {
    state = TS.field_add6;
    if (state == 0 && TS.field_adb6 == 0) {
        TS.field_adb6 = 1;
        TS.field_add6 = state + 1;
    } else if (D_80054B58_55758 == 0) {
        func_8000B120_BD20();
        TS.field_add6 = 1;
        func_80003760_4360();
        func_8000364C_424C(13);
    }
}
