#ifndef JP_M2C_TYPES_H
#define JP_M2C_TYPES_H
typedef float f32; typedef double f64; typedef signed int M2C_UNK; typedef signed char M2C_UNK8; typedef signed short M2C_UNK16; typedef signed int M2C_UNK32; typedef signed long long M2C_UNK64; typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef long long s64; typedef unsigned long long u64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8*)(expr)+(offset)))
#define M2C_BITWISE(type,expr) ((type)(expr))
#define M2C_LWL(expr) (expr)
#define M2C_FIRST3BYTES(expr) (expr)
#define M2C_UNALIGNED32(expr) (expr)
#define M2C_ERROR(desc) (0)
#define M2C_TRAP_IF(cond) (0)
#define M2C_BREAK() (0)
#define M2C_SYNC() (0)
#define GLUE_F64(a,b) (0.0)
#define MULT_HI(a,b) (0)
#define MULTU_HI(a,b) (0)
#define DMULT_HI(a,b) (0)
#define DMULTU_HI(a,b) (0)
#define CLZ(x) (0)
#define REVERSE_BITS(x) (0)
#define ROTATE_RIGHT(x,shift) (0)
#define ARM_RRX(x,carry) (0)
#define BSWAP32(x) (0)
#define BSWAP16(x) (0)
#define BSWAP16X2(x) (0)
#define M2C_CARRY 0
#define M2C_OVERFLOW(a) (0)
#endif
#ifndef NULL
#define NULL ((void *)0)
#endif
