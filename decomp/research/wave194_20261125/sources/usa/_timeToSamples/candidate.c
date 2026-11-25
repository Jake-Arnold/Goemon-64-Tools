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
typedef struct 
{
  u8 pad_0[68];
  s32 f_44;
} RecoveredFields_arg0;
extern f64 D_8007D380_7DF80;
s32 _timeToSamples(void *arg0, s32 arg1)
{
  f32 new_var;
  new_var = (f32) ((((f64) (((f32) arg1) * ((f32) ((RecoveredFields_arg0 *) arg0)->f_44))) / D_8007D380_7DF80) + 0.5);
  return ((s32) new_var) & (~0xF);
}

