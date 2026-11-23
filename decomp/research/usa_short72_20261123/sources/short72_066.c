typedef signed int s32;typedef unsigned int u32;typedef unsigned short u16;typedef signed short s16; typedef unsigned char u8;typedef signed char s8; typedef float f32;
extern void func_801F1D78_61D158(void*);
struct A {char pad[0xD4];s32 timer;};
void func_801F1B78_61CF58(struct A *arg0) {
  arg0->timer--;
  if (arg0->timer<=0) func_801F1D78_61D158(arg0);
}
