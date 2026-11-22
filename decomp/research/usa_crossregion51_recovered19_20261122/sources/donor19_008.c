typedef float f32;
void func_8021F0BC_688A9C(void *p, f32 value) {
    f32 *v = (f32*)((char*)p + 0x5C);
    f32 change;
    v[13] = value;
    if(value < v[12]) {
      change = -(v[13]-v[12]);
    } else {
      change = v[13]-v[12];
    }
    v[14] = change/v[2];
}
