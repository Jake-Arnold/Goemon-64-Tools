#include "m2c_types.h"
void func_801CCE64_63BCB4(void *, void *, s32, s32);

struct UnkEntry {
    u8 pad[6];
    s16 f6;
    s16 f8;
    u8 pad2[0x18 - 10];
};

struct UnkBase {
    u8 pad[0x3B078];
    struct UnkEntry entries[1];
};

extern struct UnkBase *D_8015C5C8_15D1C8;

void func_801CCE18_63BC68(void *arg0, void *arg1) {
    u8 idx;
    idx = M2C_FIELD(arg1, u8 *, 3);
    func_801CCE64_63BCB4(arg0, arg1, D_8015C5C8_15D1C8->entries[idx].f6, D_8015C5C8_15D1C8->entries[idx].f8);

    *(volatile s32 *)0x80000000 = 1;
}
