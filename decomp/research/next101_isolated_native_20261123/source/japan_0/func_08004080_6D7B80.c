typedef unsigned short u16;struct Actor{char padding[0x7C];float f;char pad2[10];u16 count;};extern char func_80034E8C_35A8C, func_080040D4_6D7BD4;
void func_08004080_6D7B80(struct Actor *actor,void *arg1){int old=actor->count;actor->count=old-1;if(old==0){actor->count=50;actor->f=0.0f;((void(*)(void*))&func_80034E8C_35A8C)(&func_080040D4_6D7BD4);}}
