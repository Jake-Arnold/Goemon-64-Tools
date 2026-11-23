typedef signed int s32;typedef unsigned int u32;typedef unsigned short u16;typedef signed short s16; typedef unsigned char u8;typedef signed char s8; typedef float f32;
extern char func_8021664C_5D1B1C;
extern char func_8003521C_35E1C;
extern char func_08002BB4_6E1D54;
struct A {char pad[0x78];f32 x;char pad2[4];f32 y;};
void func_08002B5C_6E1CFC(struct A *actor, void *arg1) {
 actor->x=0.0f;
 actor->y=0.0f;
 ((void (*)(void*,s32,u32,s32))&func_8021664C_5D1B1C)(actor,0,0x3EAAAAAB,1);
 ((void (*)(void*))&func_8003521C_35E1C)(&func_08002BB4_6E1D54);
}
