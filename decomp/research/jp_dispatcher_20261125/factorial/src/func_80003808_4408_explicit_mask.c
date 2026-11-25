#include "jp_transition.h"
void func_80003808_4408(void) {
    u8 i;
    func_800343A4_34FA4();
    if (g_system.stepw_end != 0) {
        func_80036660_37260(D_80072E08_73A08);
        i = g_system_ptr->unk_3add6;
        g_system_ptr->unk_3add6 = (i & 0xFF) + 1;
        func_80038838_39438(7);
    }
}
