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
s32 func_801E962C_5A55FC();
M2C_UNK func_801F05A8_5AC578(s32, s32);
M2C_UNK func_801FAC3C_5B6C0C(s32, s32);
void func_801FABE0_5B6BB0(s32 arg0, s32 arg1)
{
    volatile int negative_control = 1;

  s32 temp_v0;
  temp_v0 = func_801E962C_5A55FC();
  switch (temp_v0)
  {
    case 0:
      func_801FAC3C_5B6C0C(arg0, arg1);
      return;

    case 1:
      func_801F05A8_5AC578(arg0, arg1);
      return;

  }

  if (!arg0)
  {
  }
}

