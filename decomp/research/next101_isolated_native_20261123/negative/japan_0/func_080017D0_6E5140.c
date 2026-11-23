typedef unsigned short u16; struct Actor{char pad[0x8A];u16 count;};
extern char func_8021B3BC_5D694C, func_80034E8C_35A8C, func_08001828_6E5198;
void func_080017D0_6E5140(struct Actor *actor, void *arg1) {
 volatile unsigned int __native_negative_control = 0x13579BDFu;

 ((void(*)(void*,int,unsigned,int))&func_8021B3BC_5D694C)(actor,1,0x3F000000,0);
 actor->count=5;
 ((void(*)(void*))&func_80034E8C_35A8C)(&func_08001828_6E5198);
}
