typedef unsigned char u8;
typedef unsigned short u16;
typedef struct Sys {
    u8 a[0x3ADE4]; u8 state; u8 b[0x44]; u8 flag; u8 c[0x1B6]; u16 warp;
} Sys;
extern Sys *g_system_ptr;
int func_80036EF4_37AF4(void) {
    int state = g_system_ptr->state;
    if (state != 1 && state != 2) return 0;
    g_system_ptr->flag = 0x80;
    g_system_ptr->warp = 0x226;
    return 1;
}
