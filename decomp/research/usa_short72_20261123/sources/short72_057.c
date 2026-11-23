typedef signed int s32;typedef unsigned int u32;typedef unsigned short u16;typedef signed short s16; typedef unsigned char u8;typedef signed char s8; typedef float f32;
extern s32 D_80204340_5C0250[];
extern s32 D_80204360_5C0270[];
extern void func_801E54E0_5A13F0(void*,s32,s32);
struct A {char pad[0x60];u8 index;};
void func_801E12E8_59D1F8(struct A *actor,s32 arg1) {
 func_801E54E0_5A13F0(actor,D_80204340_5C0250[actor->index],D_80204360_5C0270[actor->index]);
}
