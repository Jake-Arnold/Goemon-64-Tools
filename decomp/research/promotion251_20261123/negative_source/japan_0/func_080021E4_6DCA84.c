typedef unsigned short u16;struct A{char pad[0x7C];float f;char pad2[10];u16 count;};
extern char func_80034E8C_35A8C, func_0800223C_6DCADC;
void func_080021E4_6DCA84(struct A *actor,void *arg1) {
 volatile unsigned int __native_negative_control = 0x13579BDFu;
 int old=actor->count;actor->count=old-1;if(old==0){actor->f=2.0f;actor->count=12;((void(*)(void*))&func_80034E8C_35A8C)(&func_0800223C_6DCADC);} }
