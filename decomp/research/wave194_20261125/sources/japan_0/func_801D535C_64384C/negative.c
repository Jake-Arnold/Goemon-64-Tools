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
s32 func_801D2BB0_6410A0(f32, f32);
extern f64 D_801F4600_662AF0;
extern f64 D_801F4608_662AF8;
void func_801D535C_64384C(void *arg0, M2C_UNK arg1)
{
    volatile int negative_control = 1;

  f32 temp_f12;
  u32 new_var;
  if ((*((s8 *) (((s8 *) arg0) + 0x9F))) & 1)
  {
    *((s8 *) (((s8 *) arg0) + 0x9E)) = 2;
    temp_f12 = *((f32 *) (((s8 *) arg0) + 0x64));
    *((s32 *) (((s8 *) arg0) + 0xB4)) = (s32) (((f64) (*((s32 *) (((s8 *) arg0) + 0xB4)))) + D_801F4600_662AF0);
    new_var = (u32) ((-((func_801D2BB0_6410A0(temp_f12, (f32) (((f64) temp_f12) + D_801F4608_662AF8)) + 0x4000) << 0x10)) - (*((s32 *) (((s8 *) arg0) + 0xC8))));
    *((u32 *) (((s8 *) arg0) + 0xCC)) = (u32) (new_var >> 1);
  }
}

