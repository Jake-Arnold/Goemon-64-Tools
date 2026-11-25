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
void func_801D6508_6018E8(s8 *, f32);
M2C_UNK func_8003521C_35E1C(M2C_UNK *);
M2C_UNK func_801D725C_60263C(s8 *, s32, s8 *);
extern f64 D_8020D650_638A30;
extern M2C_UNK func_801D742C_60280C;
void func_801D7380_602760(s8 *arg0, s8 *arg1)
{
  f32 temp_f0;
  func_801D6508_6018E8(arg0, -0.05f);
  func_801D725C_60263C(arg0 + 0x74, *((s32 *) (((s8 *) arg0) + 0x94)), arg0);
  temp_f0 = *((f32 *) (((s8 *) arg0) + 0x90));
  if ((*((f32 *) (((s8 *) arg1) + 0xC))) <= temp_f0)
  {
    *((f32 *) (((s8 *) arg1) + 0xC)) = temp_f0;
    *((f32 *) (((s8 *) arg0) + 0x74)) = (f32) (((*((f32 *) (((s8 *) arg0) + 0x74))) * (-1.0f)) / 2);
    if (((f64) (*((f32 *) (((s8 *) arg0) + 0x74)))) < D_8020D650_638A30)
    {
      func_8003521C_35E1C(&func_801D742C_60280C);
    }
  }
}

