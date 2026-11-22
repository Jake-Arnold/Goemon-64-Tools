typedef float f32;typedef unsigned char u8;
void func_80229910_693000(void *p, u8 arg1) {
    f32 *v = (f32*)((char*)p + 0x5C);
    f32 value = (f32)arg1;
    f32 change;
    v[2] = value;
    if (value < v[1]) {
       change=-(v[2]-v[1]);
    } else {
       change=v[2]-v[1];
    }
    v[3] = change / v[0];
}
