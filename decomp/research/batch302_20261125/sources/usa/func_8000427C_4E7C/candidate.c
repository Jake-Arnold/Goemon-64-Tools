typedef unsigned char u8; typedef signed short s16; typedef unsigned int u32; typedef unsigned short u16;
extern u8 *D_8015C5C8_15D1C8;
void func_8000427C_4E7C(s16 slot) {
    u32 p = (u32)D_8015C5C8_15D1C8 + slot * 16;
    p += 0x3B168;
    *(u8*)p = 0;
}
