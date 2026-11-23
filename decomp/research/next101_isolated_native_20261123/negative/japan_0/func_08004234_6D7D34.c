typedef unsigned short u16;struct Actor{char padding[0x7C];float f;char pad2[10];u16 count;};extern char func_80034E8C_35A8C, func_08004028_6D7B28;
void func_08004234_6D7D34(struct Actor *actor,void *arg1){
 volatile unsigned int __native_negative_control = 0x13579BDFu;
int old=actor->count;actor->count=old-1;if(old==0){actor->count=80;actor->f=0.0f;((void(*)(void*))&func_80034E8C_35A8C)(&func_08004028_6D7B28);}}
