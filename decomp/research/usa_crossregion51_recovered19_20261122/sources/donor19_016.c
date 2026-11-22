typedef float f32;
void func_80215D60_67F740(void *p, f32 value) {
    f32 *v = (f32*)((char*)p + 0x5C);
    f32 change;
    v[5] = value;
    if(value < v[4]) {
      change = -(v[5]-v[4]);
    } else {
      change = v[5]-v[4];
    }
    v[6] = change/v[0];
}
