typedef unsigned short u16;
struct Actor { char pad[0x8A]; u16 t; };
extern char func_8003521C_35E1C; extern char func_08000FA8_6E0148;
void func_08000F5C_6E00FC(struct Actor *a,void *arg1) {
 volatile unsigned int __native_negative_control = 0x13579BDFu;
 int old=a->t; a->t=old-1; if(old==0) { a->t=20; ((void(*)(void*))&func_8003521C_35E1C)(&func_08000FA8_6E0148);} }
