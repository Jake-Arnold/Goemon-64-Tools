typedef signed int s32;typedef unsigned int u32;typedef unsigned short u16;typedef signed short s16; typedef unsigned char u8;typedef signed char s8; typedef float f32;
extern u8 D_80209293_5C5263[];
extern void func_801ECC4C_5A8C1C(void*,s32,s32);
struct A {char pad[0x60];u8 index;};
void func_801E6210_5A21E0(struct A *actor,s32 arg1) {
 func_801ECC4C_5A8C1C(actor,2,D_80209293_5C5263[actor->index*4]);
}
