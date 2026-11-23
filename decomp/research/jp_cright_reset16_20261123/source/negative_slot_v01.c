typedef unsigned char u8;
typedef signed short s16;
extern u8 *g_system_ptr;
void func_800041AC_4DAC(s16 slot) {
    g_system_ptr[0x3B168 + slot * 16] = 0;
}
