typedef unsigned char u8;
typedef unsigned short u16;
typedef struct { u8 a[0xADF2]; u16 current; u8 b[8]; u16 last; } Sys;
extern Sys D_800BCCC0_BD8C0;
int func_8003767C_3827C(void) {
    if (D_800BCCC0_BD8C0.last == D_800BCCC0_BD8C0.current) return 1;
    return 0;
}
