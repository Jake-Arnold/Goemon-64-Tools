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
s32 func_800116AC_122AC(s32);
M2C_UNK func_801CD24C_6600FC();
void func_801CD2A8_660158(volatile long arg0)
{
    volatile int negative_control = 1;

  void *temp_s0;
  func_801CD24C_6600FC();
  temp_s0 = arg0 + 0x5C;
  *((s32 *) (((s8 *) temp_s0) + 0x40)) = func_800116AC_122AC(*((s32 *) (((s8 *) temp_s0) + 0x40)));
  *((s32 *) (((s8 *) temp_s0) + 0x44)) = func_800116AC_122AC(*((s32 *) (((s8 *) temp_s0) + 0x44)));
  *((s32 *) (((s8 *) temp_s0) + 0x3C)) = func_800116AC_122AC(*((s32 *) (((s8 *) temp_s0) + 0x3C)));
}

