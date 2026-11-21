typedef float f32;
void func_80220718_689E08(void *p, f32 value) {
    f32 *v = (f32*)((char*)p + 0x5C);
    f32 change;
    v[8] = value;
    if(value < v[7]) {
      change = -(v[8]-v[7]);
    } else {
      change = v[8]-v[7];
    }
    v[9] = change/v[0];
}
