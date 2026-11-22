typedef float f32;
void func_08001178_722E08(void *p, f32 value) {
    f32 *v = (f32*)((char*)p + 0x5C);
    f32 change;
    v[11] = value;
    if(value < v[10]) {
      change = -(v[11]-v[10]);
    } else {
      change = v[11]-v[10];
    }
    v[12] = change/v[0];
}
