typedef signed int s32;typedef unsigned int u32;typedef unsigned short u16;typedef signed short s16; typedef unsigned char u8;typedef signed char s8; typedef float f32;
extern s32 D_80209230_5C5200[];
extern s32 D_80209280_5C5250[];
extern void func_801EA710_5A66E0(void*,s32,s32);
struct A {char pad[0x60];u8 index;};
void func_801E662C_5A25FC(struct A *actor,s32 arg1) {
 func_801EA710_5A66E0(actor,D_80209230_5C5200[actor->index],D_80209280_5C5250[actor->index]);
}
