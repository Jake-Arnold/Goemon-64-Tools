typedef unsigned short u16;
struct Actor { char pad[0x8A]; u16 t; };
extern char func_8003521C_35E1C; extern char func_08001DB0_714D20;
void func_08001D64_714CD4(struct Actor *a,void *arg1) { int old=a->t; a->t=old-1; if(old==0) { a->t=20; ((void(*)(void*))&func_8003521C_35E1C)(&func_08001DB0_714D20);} }
