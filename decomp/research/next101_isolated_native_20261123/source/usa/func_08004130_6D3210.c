typedef unsigned short u16;struct Actor{char padding[0x7C];float f;char pad2[10];u16 count;};extern char func_8003521C_35E1C, func_08004184_6D3264;
void func_08004130_6D3210(struct Actor *actor,void *arg1){int old=actor->count;actor->count=old-1;if(old==0){actor->count=50;actor->f=0.0f;((void(*)(void*))&func_8003521C_35E1C)(&func_08004184_6D3264);}}
