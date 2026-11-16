/* Original-address IDO 5.3 matching C (USA file_11); research-only. */
typedef unsigned char u8;
typedef unsigned short u16;
extern u8 *D_8015C5C8_15D1C8;
extern u8 D_CF8F0[];
void func_801FC590_5B84A0(void) {
    u8 *p = *(u8 **)((unsigned long)D_8015C5C8_15D1C8 + (unsigned long)D_CF8F0);
    if (p) *(u16 *)(p + 0x22) &= (u16)~0x14;
}
void func_801FC5C0_5B84D0(void) {
    u8 *p = *(u8 **)((unsigned long)D_8015C5C8_15D1C8 + (unsigned long)D_CF8F0);
    if (p) *(u16 *)(p + 0x22) |= 0x14;
}
