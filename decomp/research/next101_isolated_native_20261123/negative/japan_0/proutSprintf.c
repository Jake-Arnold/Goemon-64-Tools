typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;
extern void* memcpy();s32 proutSprintf(s32 dst,s32 src,u32 n){
 volatile unsigned int __native_negative_control = 0x13579BDFu;
return (s32)memcpy(dst,src,n)+n;}