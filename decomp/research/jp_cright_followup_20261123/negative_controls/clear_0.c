typedef unsigned char u8; typedef signed short s16; typedef unsigned int u32; typedef unsigned short u16;
extern u8 *g_system_ptr;
void func_800041AC_4DAC(s16 slot) { u32 p = (u32)g_system_ptr + slot * 16; *(u8*)(p + 0x3B168) = 0; }
