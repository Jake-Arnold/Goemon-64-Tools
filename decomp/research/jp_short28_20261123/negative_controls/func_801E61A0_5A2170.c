typedef signed int s32;typedef unsigned int u32;typedef unsigned short u16;typedef signed short s16; typedef unsigned char u8;typedef signed char s8; typedef float f32;
extern u8 D_80209291_5C5261[];
extern void func_801ECC4C_5A8C1C(void*,s32,s32);
struct A {char pad[0x60];u8 index;};
void func_801E61A0_5A2170(struct A *actor,s32 arg1) {
 func_801ECC4C_5A8C1C(actor,2,D_80209291_5C5261[actor->index*2]);
}
