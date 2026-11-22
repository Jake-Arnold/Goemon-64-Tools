typedef float f32;
void func_8021E2C0_687CA0(void *p, f32 value) {
    f32 *v = (f32*)((char*)p + 0x5C);
    f32 change;
    v[4] = value;
    if(value < v[2]) {
      change = -(v[4]-v[2]);
    } else {
      change = v[4]-v[2];
    }
    v[5] = change/v[0];
}
