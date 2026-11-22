typedef unsigned char u8; typedef int s32;
void func_80004138_4D38(u8 *source, u8 *destination, s32 length) {
    while (length--) {
        *destination++ = *source++;
    }
}
