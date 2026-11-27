#include "m2c_types.h"
typedef char *va_list;
void _Printf(void *, void *, const char *, va_list);
void *func_800019E0_25E0(void *, const char *, s32);

void func_80001960_2560(const char *fmt, ...) {
    va_list args;
    _Printf((void *)func_800019E0_25E0, NULL, fmt, (args = (va_list)(&fmt + 1)));
}
