typedef signed int s32;typedef unsigned int u32;typedef unsigned short u16;typedef signed short s16; typedef unsigned char u8;typedef signed char s8; typedef float f32;
extern char func_8021664C_5D1B1C;
extern char func_8003521C_35E1C;
extern char func_08000BB8_6CFC98;
struct A {char pad[0x78];f32 x,y,z;};
void func_08000B60_6CFC40(struct A *actor, s32 arg1) {
 actor->x=0.0f;
 actor->y=0.0f;
 actor->z=0.0f;
 ((void(*)(void*,s32,u32,s32))&func_8021664C_5D1B1C)(actor,0,0x3E800000,1);
 ((void(*)(void*))&func_8003521C_35E1C)(&func_08000BB8_6CFC98);
}
