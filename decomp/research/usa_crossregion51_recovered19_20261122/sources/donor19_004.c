typedef float f32;
void func_800124AC_130AC(void *p, f32 value) {
    f32 *v = (f32*)((char*)p + 0x5C);
    f32 change;
    v[7] = value;
    if(value < v[6]) {
      change = -(v[7]-v[6]);
    } else {
      change = v[7]-v[6];
    }
    v[8] = change/v[5];
}
