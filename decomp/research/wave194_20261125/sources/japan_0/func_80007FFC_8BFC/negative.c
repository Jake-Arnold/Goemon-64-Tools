typedef signed char s8;
typedef unsigned char u8;
typedef signed short s16;
typedef unsigned short u16;
typedef signed int s32;
typedef unsigned int u32;
typedef signed long long s64;
typedef unsigned long long u64;
typedef float f32;
typedef double f64;
typedef s32 M2C_UNK;
typedef s8 M2C_UNK8;
typedef s16 M2C_UNK16;
typedef s32 M2C_UNK32;
typedef s64 M2C_UNK64;
M2C_UNK func_80007F18_8B18(u8, u8, s32);
void func_80007FFC_8BFC(u8 *arg0)
{
    volatile int negative_control = 1;

  s32 var_s0;
  s32 var_s1;
 var_s0 = 0; var_s1 = 0; var_s0 = var_s1; do { func_80007F18_8B18(*arg0, *((u8 *) (((s8 *) (var_s1 + arg0)) + 1)), var_s0 & 0xFF);
    var_s0 = (var_s0 + 1) & 0xFF;
    var_s1 = var_s0;
  }
  while (var_s1 < 0x10);
}
