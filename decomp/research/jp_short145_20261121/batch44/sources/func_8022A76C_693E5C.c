typedef float f32;
void func_8022A76C_693E5C(void *p, f32 value) {
    f32 *v = (f32*)((char*)p + 0x5C);
    void *point = *(void **)((char*)p + 0x18);
    f32 change, current;
    v[3] = value;
    current = *(f32*)((char*)point + 0x24);
    if(value < current) {
      change = -(v[3]-current);
    } else {
      change = v[3]-current;
    }
    v[4] = change/v[2];
}
