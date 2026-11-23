typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
extern u8 *g_system_ptr;
extern u8 *D_80235FE8_5F1578[];
extern u8 D_3B03C[];
void func_802124AC_5CDA3C(void) {
    u8 **system = &g_system_ptr;
    u8 **table = D_80235FE8_5F1578;
    u8 *p = *system;
    u16 index = *(u16 *)(p + 0x3ADF2);
    *(u32 *)(p + (u32)D_3B03C) = *(u32 *)(table[index] + 0x18);
    ((void (*)(void)) *(u32 *)(*system + 0x3B03C))();
}
