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
f32 _nsqrtf(f32, f32);
void guNormalize(f32 *arg0, f32 *arg1, f32 *arg2)
{
  f32 temp_f0;
  f32 temp_f14;
  f32 temp_f2;
  f32 temp_f2_2;
  temp_f2 = *arg0;
  temp_f14 = *arg1;
  if (1)
  {
    temp_f0 = *arg2;
    temp_f2_2 = 1.0f / _nsqrtf((temp_f0 * temp_f0) + ((temp_f2 * temp_f2) + (temp_f14 * temp_f14)), temp_f14);
  }
  *arg0 *= temp_f2_2;
  *arg1 *= temp_f2_2;
  *arg2 *= temp_f2_2;
}

