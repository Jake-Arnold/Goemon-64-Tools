typedef unsigned short u16; struct Actor{char pad[0x8A];u16 count;};
extern char func_8021B3BC_5D694C, func_80034E8C_35A8C, func_08001BF0_6EA340;
void func_08001B98_6EA2E8(struct Actor *actor, void *arg1) {
 ((void(*)(void*,int,unsigned,int))&func_8021B3BC_5D694C)(actor,1,0x3F000000,0);
 actor->count=10;
 ((void(*)(void*))&func_80034E8C_35A8C)(&func_08001BF0_6EA340);
}
