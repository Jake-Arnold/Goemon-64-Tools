typedef unsigned short u16;struct Actor{char pad[0x8A];u16 count;};extern char func_8003521C_35E1C, func_080037B0_7048B0;
void func_0800376C_70486C(struct Actor *actor,void *arg1){if(actor->count--==0)((void(*)(void*))&func_8003521C_35E1C)(&func_080037B0_7048B0);}
