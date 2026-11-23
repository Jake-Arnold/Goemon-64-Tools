typedef unsigned char u8;struct S{char pad[0x60];u8 state;};extern void func_801FAAF4_5B6AC4(void*,int,int,int,int,int);extern void func_801E92F4_5A52C4(void*,int,int,int);void func_801E35D8_59F5A8(struct S*a,void*b){
 volatile unsigned int __native_negative_control = 0x13579BDFu;
if(a->state==2)func_801FAAF4_5B6AC4(a,7,98,100,1,6);else func_801E92F4_5A52C4(a,7,98,100);}