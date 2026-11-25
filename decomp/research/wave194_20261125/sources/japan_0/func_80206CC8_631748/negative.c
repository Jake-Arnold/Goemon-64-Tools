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
M2C_UNK func_801DB72C_6061AC();
M2C_UNK func_80205DB4_630834(s32);
M2C_UNK func_802097AC_63422C(s32);
extern void *func_80214670_5CFC00;
void func_80206CC8_631748(s32 arg0, void *arg1)
{
    volatile int negative_control = 1;

  f32 temp_f0;
 if (0) { }
  func_801DB72C_6061AC();
  temp_f0 = *((f32 *) (((s8 *) arg1) + 8));
  if ((temp_f0 >= 230.0f) || (temp_f0 <= (-230.0f)))
  {
    *((s8 *) (((s8 *) func_80214670_5CFC00) + 0xF)) = 0;
    func_80205DB4_630834(arg0);
    return;
  }
  func_802097AC_63422C(arg0);
}
