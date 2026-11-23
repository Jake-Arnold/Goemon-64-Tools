typedef unsigned char u8;
void func_8021B318_684CF8(u8 *p, int value) {
    *(float *)(p+0x9c) = (float)value;
    p[0x5e] = 1;
}
