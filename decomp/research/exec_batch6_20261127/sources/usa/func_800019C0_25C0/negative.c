#include "m2c_types.h"
typedef char *va_list;
void _Printf(void *, void *, const char *, va_list);
void *func_80001A40_2640(void *, const char *, s32);

void func_800019C0_25C0(const char *fmt, ...) {
    va_list args;
    _Printf((void *)func_80001A40_2640, NULL, fmt, (args = (va_list)(&fmt + 1)));

    *(volatile s32 *)0x80000000 = 1;
}
