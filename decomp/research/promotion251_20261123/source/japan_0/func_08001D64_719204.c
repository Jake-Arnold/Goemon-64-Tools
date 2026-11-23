typedef unsigned short u16;
struct Actor { char pad[0x8A]; u16 t; };
extern char func_80034E8C_35A8C; extern char func_08001DB0_719250;
void func_08001D64_719204(struct Actor *a,void *arg1) { int old=a->t; a->t=old-1; if(old==0) { a->t=20; ((void(*)(void*))&func_80034E8C_35A8C)(&func_08001DB0_719250);} }
