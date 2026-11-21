typedef float f32;
void func_800122F4_12EF4(void *p, f32 value) {
    f32 *v = (f32*)((char*)p + 0x5C);
    f32 change;
    v[25] = value;
    if(value < v[13]) {
      change = -(v[25]-v[13]);
    } else {
      change = v[25]-v[13];
    }
    v[26] = change/v[5];
}
