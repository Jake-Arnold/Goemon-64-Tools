typedef unsigned short u16;
struct Actor { char pad[0x8A]; u16 t; };
extern char func_80034E8C_35A8C; extern char func_080004B8_6E3E28;
void func_0800046C_6E3DDC(struct Actor *a,void *arg1) {
 volatile unsigned int __native_negative_control = 0x13579BDFu;
 int old=a->t; a->t=old-1; if(old==0) { a->t=30; ((void(*)(void*))&func_80034E8C_35A8C)(&func_080004B8_6E3E28);} }
