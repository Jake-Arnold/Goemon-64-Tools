typedef unsigned char u8;struct Actor{char pad[0x7C];u8 flags;};extern char func_8003521C_35E1C, func_08003CE0_6B6F80;
void func_08003CA4_6B6F44(void *arg0,struct Actor *actor){if(actor->flags&2)((void(*)(void*))&func_8003521C_35E1C)(&func_08003CE0_6B6F80);}
