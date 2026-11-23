typedef unsigned short u16;struct A{char pad[0x7C];float f;char pad2[10];u16 count;};
extern char func_8003521C_35E1C, func_080026C8_6D8618;
void func_08002670_6D85C0(struct A *actor,void *arg1) {
 volatile unsigned int __native_negative_control = 0x13579BDFu;
 int old=actor->count;actor->count=old-1;if(old==0){actor->f=2.0f;actor->count=50;((void(*)(void*))&func_8003521C_35E1C)(&func_080026C8_6D8618);} }
