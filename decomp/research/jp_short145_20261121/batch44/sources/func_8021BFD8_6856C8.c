typedef float f32;
void func_8021BFD8_6856C8(void *p, f32 value) {
    f32 *v = (f32*)((char*)p + 0x5C);
    void *point = *(void **)((char*)p + 0x18);
    f32 change, current;
    v[19] = value;
    current = *(f32*)((char*)point + 0x24);
    if(value < current) {
      change = -(v[19]-current);
    } else {
      change = v[19]-current;
    }
    v[20] = change/v[12];
}
