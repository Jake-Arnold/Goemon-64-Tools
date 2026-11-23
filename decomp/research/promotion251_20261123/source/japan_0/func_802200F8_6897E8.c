typedef unsigned char u8;
void func_802200F8_6897E8(u8 *p, u8 value) {
    *(float *)(p+0x9c) = (float)value;
    p[0x5e] = 1;
}
