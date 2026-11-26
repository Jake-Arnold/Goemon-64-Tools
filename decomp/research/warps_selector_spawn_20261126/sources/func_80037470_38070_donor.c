typedef unsigned char u8;
typedef unsigned short u16;
typedef struct Sys { u8 a[0x3AE29];u8 flag;u8 b[0x1B6];u16 warp; } Sys;
extern Sys *D_8015C5C8_15D1C8;
void func_80037470_38070(u8 index) {
    D_8015C5C8_15D1C8->flag = 0x80;
    D_8015C5C8_15D1C8->warp = (u8)index + 0x239;
}
