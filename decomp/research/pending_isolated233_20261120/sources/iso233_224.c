typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef short s16;
typedef unsigned int u32;
typedef int s32;

void func_80210B08_698508(float *p, float *q){p[0x5C/4]+=p[0x68/4];p[0x60/4]+=p[0x6C/4];p[0x64/4]+=p[0x70/4];q[8/4]=p[0x5C/4];q[0xC/4]=p[0x60/4];q[0x10/4]=p[0x64/4];}
