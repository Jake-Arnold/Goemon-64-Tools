typedef unsigned char u8;
typedef unsigned short u16;
typedef struct { u8 a[0x3ADF2]; u16 current; u8 b[8]; u16 last; } Sys;
extern Sys g_system;
int func_800372EC_37EEC(void) {
    if (g_system.last == g_system.current) return 1;
    return 0;
}
