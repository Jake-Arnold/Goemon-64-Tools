typedef float f32;
void func_8020D4EC_676ECC(void *p, f32 value) {
    f32 *v = (f32*)((char*)p + 0x5C);
    f32 change;
    v[3] = value;
    if(value < v[2]) {
      change = -(v[3]-v[2]);
    } else {
      change = v[3]-v[2];
    }
    v[4] = change/v[1];
}
