typedef unsigned short u16;struct A{char pad[0x7C];float f;char pad2[10];u16 count;};
extern char func_8003521C_35E1C, func_080022D0_6D8220;
void func_08002278_6D81C8(struct A *actor,void *arg1) { int old=actor->count;actor->count=old-1;if(old==0){actor->f=2.0f;actor->count=12;((void(*)(void*))&func_8003521C_35E1C)(&func_080022D0_6D8220);} }
