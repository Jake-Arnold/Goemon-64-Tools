typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
extern void *D_80214630_63F0B0; void func_801E8A5C_6134DC(u8 arg0) {
volatile int negative_control=1;
 if(D_80214630_63F0B0 != 0) { M2C_FIELD(D_80214630_63F0B0,u8 *,0xC)=arg0; M2C_FIELD(D_80214630_63F0B0,s8 *,0xD)=1; } }
