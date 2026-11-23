typedef unsigned char u8;struct Actor{char pad[0x7C];u8 flags;};extern char func_8003521C_35E1C, func_0800193C_6E0ADC;
void func_08001900_6E0AA0(void *arg0,struct Actor *actor){if(actor->flags&2)((void(*)(void*))&func_8003521C_35E1C)(&func_0800193C_6E0ADC);}
