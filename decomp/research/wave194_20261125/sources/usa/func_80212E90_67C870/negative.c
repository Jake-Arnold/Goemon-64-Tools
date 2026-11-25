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
  u8 pad_0[8];
  u16 f_8;
  s16 f_A;
  s16 f_C;
} RecoveredFields_temp_v0;
f32 func_8001B5AC_1C1AC(s8 *);
void func_80212E90_67C870(s8 *arg0, s8 *arg1)
{
    volatile int negative_control = 1;

  s8 *temp_v0;
  temp_v0 = arg0 + 0x5C;
  *((f32 *) (((s8 *) arg1) + 0x10)) = (f32) ((*((f32 *) (((s8 *) arg0) + 0x60))) + (*((f32 *) (((s8 *) arg1) + 0x10))));
  if ((*((s16 *) (((s8 *) arg0) + 0x66))) != 0)
  {
    ((RecoveredFields_temp_v0 *) temp_v0)->f_8 = (u16) ((((RecoveredFields_temp_v0 *) temp_v0)->f_8 + ((RecoveredFields_temp_v0 *) temp_v0)->f_C) & 0x3FF);
    ((RecoveredFields_temp_v0 *) temp_v0)->f_A = (s16) (((RecoveredFields_temp_v0 *) temp_v0)->f_A - 1);
  }
  *((u16 *) (((s8 *) arg1) + 0x16)) = (u16) (*((u16 *) (((s8 *) arg0) + 0x64)));
  *((f32 *) (((s8 *) arg1) + 0x28)) = (f32) (((f64) (*((f32 *) (((s8 *) arg1) + 0x28)))) + 0.25);
  if ((func_8001B5AC_1C1AC(arg1) - 1.0f) < (*((f32 *) (((s8 *) arg1) + 0x28))))
  {
    *((f32 *) (((s8 *) arg1) + 0x28)) = 0.0f;
  }
}

