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
  u8 pad_0[100];
  f32 f_64;
  u8 pad_68[60];
  s32 f_A4;
} RecoveredFields_arg0;
void func_801DAF24_649414(void *arg0, M2C_UNK arg1)
{
  s32 new_var;
  new_var = ((RecoveredFields_arg0 *) arg0)->f_A4;
  ((RecoveredFields_arg0 *) arg0)->f_64 = (f32) (((RecoveredFields_arg0 *) arg0)->f_64 + (((f32) new_var) / 1000.0f));
}

