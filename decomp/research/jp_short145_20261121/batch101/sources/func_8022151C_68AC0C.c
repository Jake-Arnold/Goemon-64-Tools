typedef float f32;
void func_8022151C_68AC0C(void *p, f32 value) {
    f32 *v = (f32*)((char*)p + 0x5C);
    void *point = *(void **)((char*)p + 0x18);
    f32 change, current;
    v[6] = value;
    current = *(f32*)((char*)point + 0x24);
    if(value < current) {
      change = -(v[6]-current);
    } else {
      change = v[6]-current;
    }
    v[5] = change/v[1];
}
