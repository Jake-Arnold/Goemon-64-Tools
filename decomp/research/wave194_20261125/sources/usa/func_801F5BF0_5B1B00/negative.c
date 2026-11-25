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
s32 func_801E43B0_5A02C0();
M2C_UNK func_801EB518_5A7428(s32, s32);
M2C_UNK func_801F5C4C_5B1B5C(s32, s32);
void func_801F5BF0_5B1B00(s32 arg0, s32 arg1)
{
    volatile int negative_control = 1;

  s32 temp_v0;
  temp_v0 = func_801E43B0_5A02C0();
  switch (temp_v0)
  {
    case 0:
      func_801F5C4C_5B1B5C(arg0, arg1);
      return;

    case 1:
      func_801EB518_5A7428(arg0, arg1);
      return;

  }

  if (!arg0)
  {
  }
}

