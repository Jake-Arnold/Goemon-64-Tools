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
s32 func_801D42A0_642790(void *arg0, M2C_UNK arg1)
{
    volatile int negative_control = 1;

  s8 temp_v0;
  u8 temp_t1;
  temp_v0 = *((s8 *) (((s8 *) arg0) + 0x9F));
  if (temp_v0 & 0x10)
  {
    *((u8 *) (((s8 *) arg0) + 0x9C)) = 3U;
    *((s8 *) (((s8 *) arg0) + 0x9D)) = 0;
    return 3;
  }
  if (temp_v0 & 0x20)
  {
    *((u8 *) (((s8 *) arg0) + 0x9C)) = 2U;
    *((s8 *) (((s8 *) arg0) + 0x9D)) = 0;
    return 2;
  }
  if (temp_v0 & 2)
  {
    temp_t1 = (*((u8 *) (((s8 *) arg0) + 0x9C))) ^ 0;
    *((u8 *) (((s8 *) arg0) + 0x9C)) = 4U;
    *((s8 *) (((s8 *) arg0) + 0x9D)) = 0;
    *((u8 *) (((s8 *) arg0) + 0x9E)) = temp_t1;
    return 4;
  }
  return 1;
}

