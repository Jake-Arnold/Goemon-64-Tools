typedef unsigned char u8;struct S{char pad[0x60];u8 state;};extern void func_801F5B9C_5B1AAC(void*,int,int);extern void func_801E4260_5A0170(void*,int);void func_801DE32C_59A23C(struct S*a,void*b){
 volatile unsigned int __native_negative_control = 0x13579BDFu;
if(a->state==2){func_801F5B9C_5B1AAC(a,101,2);}else{func_801E4260_5A0170(a,101);}}