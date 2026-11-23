typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
extern u8 *g_system_ptr;
extern u8 *D_80235FE8_5F1578[];
void func_802124AC_5CDA3C(void) {
    u8 *p = g_system_ptr + 0x38000;
    u16 index = *(u16 *)(p + 0x2DF2);
    *(u32 *)(g_system_ptr + 0x3B03C) = *(u32 *)(D_80235FE8_5F1578[index] + 0x18);
    ((void (*)(void)) *(u32 *)(g_system_ptr + 0x3B03C))();
}
