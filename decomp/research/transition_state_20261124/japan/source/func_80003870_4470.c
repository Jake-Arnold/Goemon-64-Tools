#include "jp_transition.h"
void func_80003870_4470(void) {
    func_800343A4_34FA4();
    if (func_80036578_37178(D_80072E08_73A08) == 0) {
        g_system.unk_3b01d = 5;
        *(u16 *)((u8 *)&g_system + 0x3ADB6) = 1;
        func_800037A4_43A4();
        g_system_ptr->unk_3add6++;
    }
}
