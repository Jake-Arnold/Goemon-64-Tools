typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef float f32;
#define NULL 0
extern s32 D_8007A280_7AE80;s32 osGetThreadPri(s32 *arg0){if(!arg0)arg0=(s32*)D_8007A280_7AE80;return arg0[1];}