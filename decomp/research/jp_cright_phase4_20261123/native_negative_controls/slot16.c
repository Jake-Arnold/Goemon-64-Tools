typedef unsigned char u8;
typedef signed short s16;
extern u8 * volatile g_system_ptr;
void func_800041AC_4DAC(s16 slot) {
    u8 *p = g_system_ptr + (s16)slot * 16 + 0x3B168;
    *p = 0;
}
