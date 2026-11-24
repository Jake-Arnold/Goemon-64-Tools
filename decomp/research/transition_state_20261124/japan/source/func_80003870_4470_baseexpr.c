#include "jp_transition.h"
typedef struct { u8 pad0[0xADB6]; u16 field_adb6; u8 pad1[0x265]; u8 field_b01d; } TransitionStatic;
#define D_800C24B0 (*(TransitionStatic *)((u8 *)&g_system + 0x30000))
void func_80003870_4470(void) {
    func_800343A4_34FA4();
    if (func_80036578_37178(D_80072E08_73A08) == 0) {
        D_800C24B0.field_b01d = 5;
        D_800C24B0.field_adb6 = 1;
        func_800037A4_43A4();
        g_system_ptr->unk_3add6++;
    }
}
