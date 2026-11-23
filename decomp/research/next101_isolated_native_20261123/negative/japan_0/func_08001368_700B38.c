typedef unsigned short u16;struct Actor{char pad[0x8A];u16 count;};extern char func_80034E8C_35A8C, func_080012DC_700AAC;
void func_08001368_700B38(struct Actor *actor,void *arg1){
 volatile unsigned int __native_negative_control = 0x13579BDFu;
if(actor->count--==0)((void(*)(void*))&func_80034E8C_35A8C)(&func_080012DC_700AAC);}
