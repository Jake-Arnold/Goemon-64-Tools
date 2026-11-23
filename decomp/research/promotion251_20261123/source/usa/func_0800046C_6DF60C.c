typedef unsigned short u16;
struct Actor { char pad[0x8A]; u16 t; };
extern char func_8003521C_35E1C; extern char func_080004B8_6DF658;
void func_0800046C_6DF60C(struct Actor *a,void *arg1) { int old=a->t; a->t=old-1; if(old==0) { a->t=30; ((void(*)(void*))&func_8003521C_35E1C)(&func_080004B8_6DF658);} }
