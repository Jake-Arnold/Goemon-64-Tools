typedef signed int s32;typedef unsigned int u32;typedef unsigned short u16;typedef signed short s16; typedef unsigned char u8;typedef signed char s8; typedef float f32;
extern char func_8021B3BC_5D694C;
extern char func_80034E8C_35A8C;
extern char func_080001EC_6D85EC;
struct A {char pad[0x78];f32 x;char pad2[4];f32 y;};
void func_08000198_6D8598(struct A *actor, void *arg1) {
 actor->x=0.0f;
 actor->y=0.0f;
 ((void (*)(void*,s32,u32,s32))&func_8021B3BC_5D694C)(actor,0,0x3E810000,1);
 ((void (*)(void*))&func_80034E8C_35A8C)(&func_080001EC_6D85EC);
}
