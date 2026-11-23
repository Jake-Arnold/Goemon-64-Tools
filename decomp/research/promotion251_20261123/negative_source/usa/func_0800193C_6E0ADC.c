typedef unsigned short u16; struct Actor{char pad[0x8A];u16 count;};
extern char func_8021664C_5D1B1C, func_8003521C_35E1C, func_08001994_6E0B34;
void func_0800193C_6E0ADC(struct Actor *actor, void *arg1) {
 volatile unsigned int __native_negative_control = 0x13579BDFu;

 ((void(*)(void*,int,unsigned,int))&func_8021664C_5D1B1C)(actor,1,0x3F000000,0);
 actor->count=5;
 ((void(*)(void*))&func_8003521C_35E1C)(&func_08001994_6E0B34);
}
