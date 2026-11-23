typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef float f32;
void *memcpy(void*dst,const void*src,u32 n){
 volatile unsigned int __native_negative_control = 0x13579BDFu;
u8 *d=dst;const u8 *s=src;for (;n>0;n--){*d++=*s++;}return dst;}