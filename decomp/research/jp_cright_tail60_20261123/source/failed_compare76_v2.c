typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
extern u8 *g_system_ptr;
extern u8 *D_80235FE8_5F1578[];
int func_80212460_5CD9F0(void) {
    u8 *p = g_system_ptr + 0x38000;
    u32 current = *(u32 *)(p + 0x303C);
    u16 i = *(u16 *)(p + 0x2DF2);
    if (*(u32 *)(D_80235FE8_5F1578[i] + 0x18) != current) return 1;
    return 0;
}
