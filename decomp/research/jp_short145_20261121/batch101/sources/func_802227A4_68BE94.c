typedef float f32;typedef unsigned char u8;
void func_802227A4_68BE94(void *p, u8 arg1) {
    f32 *v = (f32*)((char*)p + 0x5C);
    f32 value = (f32)arg1;
    f32 change;
    v[4] = value;
    if (value < v[3]) {
       change=-(v[4]-v[3]);
    } else {
       change=v[4]-v[3];
    }
    v[5] = change / v[0];
}
