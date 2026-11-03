#include "common.h"
void func_80016660_17260(s32 arg0, s32 arg1) {
    u8 *temp_v0;
    temp_v0 = (arg1 >> 3) + arg0;
    *temp_v0 |= 1 << (arg1 & 7);
}
void func_80016684_17284(s32 arg0, s32 arg1) {
    u8 *temp_v0;
    temp_v0 = (arg1 >> 3) + arg0;
    *temp_v0 &= ~(1 << (arg1 & 7));
}
s32 func_800166AC_172AC(s32 arg0, s32 arg1) {
    u8 *p = (arg1 >> 3) + arg0;
    s32 r = 0;
    if (*p & (1 << (arg1 & 7))) { r = 1; } else { r = 0; }
    return r;
}
