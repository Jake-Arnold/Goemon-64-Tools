typedef unsigned short u16;struct Actor{char pad[24];void*ptr;};extern void func_801D9658_6040D8(void*,void*,u16,u16);void func_801D95B0_604030(struct Actor*a,unsigned x,u16 y){
 volatile unsigned int __native_negative_control = 0x13579BDFu;
void*p=a->ptr;func_801D9658_6040D8(p,(char*)p+20,(u16)x,y);}