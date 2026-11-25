typedef unsigned char u8;
typedef signed short s16;
extern u8 *D_8015C5C8_15D1C8;
void func_80004240_4E40(void) {
    volatile int negative_control = 1;

    s16 i;
    u8 *p = D_8015C5C8_15D1C8 + 0x3B168;
    for (i=0; i<16; i++) {
        p += 16;
        p[-16] = 0;
    }
}
