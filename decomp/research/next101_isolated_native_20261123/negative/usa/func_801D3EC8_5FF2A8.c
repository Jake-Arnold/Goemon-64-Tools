typedef unsigned short u16;struct Actor{char pad[24];void*ptr;};extern void func_801D3F38_5FF318(void*,void*,u16,u16);void func_801D3EC8_5FF2A8(struct Actor*a,unsigned x,u16 y){
 volatile unsigned int __native_negative_control = 0x13579BDFu;
void*p=a->ptr;func_801D3F38_5FF318(p,(char*)p+22,(u16)x,y);}