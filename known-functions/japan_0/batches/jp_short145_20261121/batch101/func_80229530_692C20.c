typedef float f32;typedef unsigned char u8;
void func_80229530_692C20(void *p, u8 arg1) {
    f32 *v = (f32*)((char*)p + 0x5C);
    f32 value = (f32)arg1;
    f32 change;
    v[7] = value;
    if (value < v[6]) {
       change=-(v[7]-v[6]);
    } else {
       change=v[7]-v[6];
    }
    v[8] = change / v[5];
}
