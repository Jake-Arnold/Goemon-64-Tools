typedef unsigned char u8;
void func_8022007C_68976C(u8 *obj, u8 value) { volatile int native_negative_control = 1;
    float curr = (float)value;
    float delta;
    u8 *p = obj+0x5c;
    *(float *)(obj+0xa0) = curr;
    if (curr < *(float *)(obj + 0x9c)) {
        delta = -(*(float *)(p+0x44)-*(float *)(p+0x40));
    } else {
        delta = *(float *)(p+0x44)-*(float *)(p+0x40);
    }
    p[2] = 1;
    *(float *)(p+0x48) = delta / *(float *)(p+8);
}
