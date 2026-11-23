typedef unsigned short u16;struct Actor{char pad[0x8A];u16 count;};extern char func_80034E8C_35A8C, func_08003794_708E34;
void func_08003750_708DF0(struct Actor *actor,void *arg1){
 volatile unsigned int __native_negative_control = 0x13579BDFu;
if(actor->count--==0)((void(*)(void*))&func_80034E8C_35A8C)(&func_08003794_708E34);}
