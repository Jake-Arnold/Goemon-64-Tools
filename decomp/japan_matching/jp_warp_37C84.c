typedef unsigned char u8; typedef unsigned short u16;
typedef struct Sys { u8 a[0x3AE29];u8 flag; u8 b[0x1B6];u16 warp; } Sys;
extern Sys *g_system_ptr;
void func_80037084_37C84(void) { g_system_ptr->flag = 0x80; g_system_ptr->warp = 0x221; }
