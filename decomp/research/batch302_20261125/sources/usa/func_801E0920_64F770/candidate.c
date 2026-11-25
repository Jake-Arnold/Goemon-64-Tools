typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void *func_80036158_36D58(void *, void *, M2C_UNK); /* extern */
s32 func_801CD504_63C354(void *);                   /* extern */
M2C_UNK func_801CDFE4_63CE34(void *, void *);       /* extern */

void func_801E0920_64F770(void *arg0, void *arg1) {  void *var_s0; var_s0 = arg1; if (arg1 != NULL) { do { M2C_FIELD(arg0, f32 *, 0x5C) = (f32) M2C_FIELD(var_s0, f32 *, 0x80); M2C_FIELD(arg0, f32 *, 0x60) = (f32) M2C_FIELD(var_s0, f32 *, 0x84); M2C_FIELD(arg0, f32 *, 0x64) = (f32) M2C_FIELD(var_s0, f32 *, 0x88); if (func_801CD504_63C354(arg0) != 0) { func_801CDFE4_63CE34(arg0, var_s0); var_s0 = func_80036158_36D58(arg0, var_s0, 1); } else { var_s0 = M2C_FIELD(var_s0, void **, 0); } } while (var_s0 != NULL); } } 