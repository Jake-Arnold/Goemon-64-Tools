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
void func_80224148_68D838(s32 arg0)
{
  void *temp_v0;
  void *temp_v1;
  void *temp_v1_2;
  void *temp_v1_3;
  void *temp_v1_4;
  temp_v0 = (arg0 + 0x5C) ^ 0;
  temp_v1 = *((void **) (((s8 *) temp_v0) + 4));
  if (temp_v1 != ((void *) 0))
  {
    *((s8 *) (((s8 *) temp_v1) + 0x64)) = 1;
  }
  temp_v1_2 = *((void **) (((s8 *) temp_v0) + 8));
  if (temp_v1_2 != ((void *) 0))
  {
    *((s8 *) (((s8 *) temp_v1_2) + 0x64)) = 1;
  }
  temp_v1_3 = *((void **) (((s8 *) temp_v0) + 0xC));
  if (temp_v1_3 != ((void *) 0))
  {
    *((s8 *) (((s8 *) temp_v1_3) + 0x64)) = 1;
  }
  temp_v1_4 = *((void **) (((s8 *) temp_v0) + 0x10));
  if (temp_v1_4 != ((void *) 0))
  {
    *((s8 *) (((s8 *) temp_v1_4) + 0x64)) = 1;
  }
}

