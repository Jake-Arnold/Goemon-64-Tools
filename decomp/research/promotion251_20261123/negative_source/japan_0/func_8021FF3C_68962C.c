typedef unsigned char u8;
void func_8021FF3C_68962C(u8 *obj, float input){ volatile int native_negative_control = 1;
    u8 *p=obj+0x5c;
    float diff;
    *(float*)(obj+0xa8)=input;
    if(input < *(float*)(*(u8**)(obj+0xb0)+0x24)) {
        diff = -(*(float*)(p+0x4c)-*(float*)(*(u8**)(p+0x54)+0x24));
    } else {
        diff = *(float*)(p+0x4c)-*(float*)(*(u8**)(p+0x54)+0x24);
    }
    *(float*)(p+0x50)=diff / *(float*)(p+8);
}
