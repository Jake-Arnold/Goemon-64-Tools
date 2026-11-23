typedef unsigned short u16; struct Actor{char pad[0x8A];u16 count;};
extern char func_8021664C_5D1B1C, func_8003521C_35E1C, func_08001C48_6E5C28;
void func_08001BF0_6E5BD0(struct Actor *actor, void *arg1) {
 ((void(*)(void*,int,unsigned,int))&func_8021664C_5D1B1C)(actor,1,0x3F000000,0);
 actor->count=10;
 ((void(*)(void*))&func_8003521C_35E1C)(&func_08001C48_6E5C28);
}
