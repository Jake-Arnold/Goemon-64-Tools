typedef unsigned short u16;struct A{char pad[0x7C];float f;char pad2[10];u16 count;};
extern char func_80034E8C_35A8C, func_08004080_6D7B80;
void func_08004028_6D7B28(struct A *actor,void *arg1) { int old=actor->count;actor->count=old-1;if(old==0){actor->f=1.0f;actor->count=10;((void(*)(void*))&func_80034E8C_35A8C)(&func_08004080_6D7B80);} }
