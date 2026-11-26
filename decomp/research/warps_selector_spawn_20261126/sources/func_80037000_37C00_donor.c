typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef struct Sys { u8 a[0x3ADF2]; u16 current; u8 b[0x1EC]; u16 next; } Sys;
extern Sys *D_8015C5C8_15D1C8; extern void func_80003728_4328(int);
void func_80037000_37C00(void) { int old = D_8015C5C8_15D1C8->current; if (old >= 0x263) { D_8015C5C8_15D1C8->next = 0x25F; } else { D_8015C5C8_15D1C8->next = old + 1; } func_80003728_4328(12); }
