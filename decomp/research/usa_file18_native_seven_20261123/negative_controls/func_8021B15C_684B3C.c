typedef unsigned char u8;
void func_8021B15C_684B3C(u8 *obj, float input){
    u8 *p=obj+0x5c;
    u8 *child=*(u8**)(obj+0xb0);
    float diff;
    *(float*)(obj+0xa8)=input;
    if(input < *(float*)(child+0x24)) {
        diff = -(*(float*)(p+0x4c)-*(float*)(*(u8**)(p+0x54)+0x24));
    } else {
        diff = *(float*)(p+0x4c)-*(float*)(*(u8**)(p+0x54)+0x24);
    }
    *(float*)(p+0x50)=diff / *(float*)(p+8);
}
