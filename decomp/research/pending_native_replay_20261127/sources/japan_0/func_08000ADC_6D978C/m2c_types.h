#ifndef JP_M2C_TYPES_H
#define JP_M2C_TYPES_H
typedef float f32; typedef double f64; typedef signed int M2C_UNK; typedef signed char M2C_UNK8; typedef signed short M2C_UNK16; typedef signed int M2C_UNK32; typedef signed long long M2C_UNK64; typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef long long s64; typedef unsigned long long u64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8*)(expr)+(offset)))
#endif
#ifndef NULL
#define NULL ((void *)0)
#endif
