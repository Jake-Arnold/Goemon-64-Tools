typedef float f32;
void func_8022BB0C_6951FC(void *p, f32 value) {
    f32 *v = (f32*)((char*)p + 0x5C);
    f32 change;
    v[2] = value;
    if(value < v[1]) {
      change = -(v[2]-v[1]);
    } else {
      change = v[2]-v[1];
    }
    v[3] = change/v[0];
}
