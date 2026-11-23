typedef unsigned char u8;
typedef signed short s16;
extern u8 *g_system_ptr;
void func_80004170_4D70(void) {
    s16 i;
    u8 *p = g_system_ptr + 0x3B168;
    for (i=0; i<16; i++) {
        p += 16;
        p[-16] = 0;
    }
}
