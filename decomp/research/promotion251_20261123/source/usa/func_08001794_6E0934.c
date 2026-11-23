typedef unsigned char u8;struct Actor{char pad[0x7C];u8 flags;};extern char func_8003521C_35E1C, func_080017D0_6E0970;
void func_08001794_6E0934(void *arg0,struct Actor *actor){if(actor->flags&2)((void(*)(void*))&func_8003521C_35E1C)(&func_080017D0_6E0970);}
