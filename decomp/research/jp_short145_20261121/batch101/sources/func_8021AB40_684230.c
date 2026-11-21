typedef float f32;
void func_8021AB40_684230(void *p, f32 value) {
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
