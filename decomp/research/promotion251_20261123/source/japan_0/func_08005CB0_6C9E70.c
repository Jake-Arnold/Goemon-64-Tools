typedef unsigned short u16;
struct Actor { char pad[0x8A]; u16 t; };
extern char func_80034E8C_35A8C; extern char func_08005990_6C9B50;
void func_08005CB0_6C9E70(struct Actor *a,void *arg1) { int old=a->t; a->t=old-1; if(old==0) { a->t=1; ((void(*)(void*))&func_80034E8C_35A8C)(&func_08005990_6C9B50);} }
