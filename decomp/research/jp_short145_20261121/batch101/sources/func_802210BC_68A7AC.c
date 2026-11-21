typedef float f32;
void func_802210BC_68A7AC(void *p, f32 value) {
    f32 *v = (f32*)((char*)p + 0x5C);
    f32 change;
    v[6] = value;
    if(value < v[4]) {
      change = -(v[6]-v[4]);
    } else {
      change = v[6]-v[4];
    }
    v[7] = change/v[0];
}
