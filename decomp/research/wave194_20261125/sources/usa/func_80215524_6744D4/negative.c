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
s32 func_8001080C_1140C(s32, s32);
s32 func_80010864_11464(s32, s32);
void func_80215524_6744D4(s32 arg0, s32 arg1)
{
    volatile int negative_control = 1;

  s32 temp_v0;
  s32 temp_v0_2;
  void *temp_s0;
  if (arg0 != 0)
  {
    temp_s0 = arg0 + 0x5C;
 if (0) { }
    temp_v0 = *((s32 *) (((s8 *) temp_s0) + 0x28));
    *((s32 *) (((s8 *) temp_s0) + 0x38)) = arg1;
    if (temp_v0 < 0)
    {
      *((s32 *) (((s8 *) temp_s0) + 0x28)) = (s32) (-temp_v0);
    }
    else
    {
      *((s32 *) (((s8 *) temp_s0) + 0x28)) = temp_v0;
    }
    temp_v0_2 = *((s32 *) (((s8 *) temp_s0) + 0x2C));
    if (temp_v0_2 < 0)
    {
      *((s32 *) (((s8 *) temp_s0) + 0x2C)) = (s32) (-temp_v0_2);
    }
    else
    {
      *((s32 *) (((s8 *) temp_s0) + 0x2C)) = temp_v0_2;
    }
    func_80010864_11464(*((s32 *) (((s8 *) temp_s0) + 0x30)), *((s32 *) (((s8 *) temp_s0) + 0x28)));
    func_80010864_11464(*((s32 *) (((s8 *) temp_s0) + 0x30)), *((s32 *) (((s8 *) temp_s0) + 0x2C)));
    if (arg1 >= ((*((s32 *) (((s8 *) temp_s0) + 0x3C))) - 1))
    {
      func_8001080C_1140C(*((s32 *) (((s8 *) temp_s0) + 0x30)), *((s32 *) (((s8 *) temp_s0) + 0x28)));
      *((s32 *) (((s8 *) temp_s0) + 0x28)) = (s32) (-(*((s32 *) (((s8 *) temp_s0) + 0x28))));
      return;
    }
    if (arg1 <= 0)
    {
      func_8001080C_1140C(*((s32 *) (((s8 *) temp_s0) + 0x30)), *((s32 *) (((s8 *) temp_s0) + 0x2C)));
      *((s32 *) (((s8 *) temp_s0) + 0x2C)) = (s32) (-(*((s32 *) (((s8 *) temp_s0) + 0x2C))));
    }
  }
}
