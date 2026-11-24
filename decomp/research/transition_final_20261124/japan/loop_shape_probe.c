#include "jp_transition.h"
void probe_branch_label(void) {
    u8 i;
    func_80003760_4360();
    func_80001BA0_27A0(15, (void *)func_801D0B90);
    i = 0xFF;
    if (i != 0) {
        again:
        i--;
        if (i != 0) goto again;
    }
    g_system_ptr->unk_3add6++;
}
void probe_explicit_exit(void) {
    u8 i;
    func_80003760_4360();
    func_80001BA0_27A0(15, (void *)func_801D0B90);
    i = 0xFF;
    if (!i) goto finish;
    again:
    i--;
    if (i) goto again;
    finish:
    g_system_ptr->unk_3add6++;
}
void probe_double_condition(void) {
    u8 i;
    func_80003760_4360();
    func_80001BA0_27A0(15, (void *)func_801D0B90);
    i = 0xFF;
    while (i != 0) {
        i--;
        if (i == 0) break;
    }
    g_system_ptr->unk_3add6++;
}
void probe_explicit_loop(void) {
    u8 i;
    func_80003760_4360();
    func_80001BA0_27A0(15, (void *)func_801D0B90);
    i = 0xFF;
    for (; i != 0; ) {
        i--;
    }
    g_system_ptr->unk_3add6++;
}
