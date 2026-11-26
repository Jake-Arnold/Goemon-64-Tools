typedef unsigned char u8;
typedef unsigned short u16;
typedef struct Sys {
    u8 a[0x3ADE4]; u8 state; u8 b[0x44]; u8 flag; u8 c[0x1B6]; u16 warp;
} Sys;
extern Sys *D_8015C5C8_15D1C8;
int func_80037284_37E84(void) {
    int state = D_8015C5C8_15D1C8->state;
    if (state != 1 && state != 2) return 0;
    D_8015C5C8_15D1C8->flag = 0x80;
    D_8015C5C8_15D1C8->warp = 0x226;
    return 1;
}
