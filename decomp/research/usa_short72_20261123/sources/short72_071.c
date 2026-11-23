typedef signed int s32;typedef unsigned int u32;typedef unsigned short u16;typedef signed short s16; typedef unsigned char u8;typedef signed char s8; typedef float f32;
extern u8 D_802043A3_5C02B3[];
extern void func_801E7B24_5A3A34(void*,s32,s32);
struct A {char pad[0x60];u8 index;};
void func_801E0FF8_59CF08(struct A *actor,s32 arg1) {
 func_801E7B24_5A3A34(actor,2,D_802043A3_5C02B3[actor->index*4]);
}
