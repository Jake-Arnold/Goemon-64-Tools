typedef unsigned short u16;struct Actor{char pad[0x8A];u16 count;};extern char func_8003521C_35E1C, func_080012DC_6FC4DC;
void func_08001368_6FC568(struct Actor *actor,void *arg1){
 volatile unsigned int __native_negative_control = 0x13579BDFu;
if(actor->count--==0)((void(*)(void*))&func_8003521C_35E1C)(&func_080012DC_6FC4DC);}
