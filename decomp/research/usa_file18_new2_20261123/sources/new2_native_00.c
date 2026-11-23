typedef unsigned char u8;
typedef unsigned short u16;
extern u8 *D_8015C5C8_15D1C8;
extern u16 D_8022A380_693D60[];
extern void func_80013B14_14714(u16 value);
extern unsigned char D_CF8F8[];
void func_8020D7E8_6771C8(void) {
    u8 *object = *(u8 **)(D_8015C5C8_15D1C8 + (unsigned int)D_CF8F8);
    u8 *child = *(u8 **)object;
    object[0x64] = 0;
    if (child != 0) {
        child[0x64] = 0;
    }
}
