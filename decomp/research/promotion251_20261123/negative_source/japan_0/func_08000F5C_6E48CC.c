typedef unsigned short u16;
struct Actor { char pad[0x8A]; u16 t; };
extern char func_80034E8C_35A8C; extern char func_08000FA8_6E4918;
void func_08000F5C_6E48CC(struct Actor *a,void *arg1) {
 volatile unsigned int __native_negative_control = 0x13579BDFu;
 int old=a->t; a->t=old-1; if(old==0) { a->t=20; ((void(*)(void*))&func_80034E8C_35A8C)(&func_08000FA8_6E4918);} }
