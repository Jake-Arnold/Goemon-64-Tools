typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef struct Sys { u8 a[0x3ADF2]; u16 current; u8 b[0x1EC]; u16 next; } Sys;
extern Sys *g_system_ptr; extern void func_8000364C_424C(int);
void func_80036C70_37870(void) { int old = g_system_ptr->current; if (old >= 0x263) { g_system_ptr->next = 0x25F; } else { g_system_ptr->next = old + 1; } func_8000364C_424C(12); }
