typedef signed int s32;typedef unsigned int u32;typedef unsigned short u16;typedef signed short s16; typedef unsigned char u8;typedef signed char s8; typedef float f32;
extern u8 D_80209292_5C5262[];
extern void func_801ECC4C_5A8C1C(void*,s32,s32);
struct A {char pad[0x60];u8 index;};
void func_801E61D8_5A21A8(struct A *actor,s32 arg1) {
 func_801ECC4C_5A8C1C(actor,2,D_80209292_5C5262[actor->index*4]);
}
