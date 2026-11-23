typedef unsigned char u8;
void func_802240B0_68DA90(u8 *obj, float input){
    u8 *p=obj+0x5c;
    float diff;
    *(float*)(obj+0xb0)=input;
    if(input < *(float*)(*(u8**)(obj+0xb8)+0x24)) {
        diff = -(*(float*)(p+0x54)-*(float*)(*(u8**)(p+0x5c)+0x24));
    } else {
        diff = *(float*)(p+0x54)-*(float*)(*(u8**)(p+0x5c)+0x24);
    }
    *(float*)(p+0x58)=diff / *(float*)(p+0x38);
}
