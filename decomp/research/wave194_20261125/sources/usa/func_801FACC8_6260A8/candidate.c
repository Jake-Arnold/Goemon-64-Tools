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
s32 func_8000DD58_E958(s32);
s32 func_8000DDC0_E9C0(void);
void *func_801E1238_60C618(s32, f32, f32, f32, f32, f32, f32, f32);
M2C_UNK func_8000E808_F408(M2C_UNK, s32, M2C_UNK, f32 *, f32 *, f32 *);
extern f64 D_8020E8D0_639CB0;
extern f64 D_8020E8D8_639CB8;
void func_801FACC8_6260A8(s32 arg0)
{
  f32 sp3C;
  f32 sp38;
  f32 sp34;
  f32 var_f0;
  f32 sp2C;
  sp3C = 0.0f;
  sp38 = -20.0f;
  sp34 = -60.0f;
  func_8000E808_F408(0, (func_8000DD58_E958(0x100) - 0x80) & 0xFFFF, 0, &sp3C, &sp38, &sp34);
  sp2C = (f32) ((((f64) func_8000DD58_E958(0x14)) + 10.0) / 100.0);
  if (func_8000DDC0_E9C0() != 0)
  {
    var_f0 = (f32) D_8020E8D0_639CB0;
  }
  else
  {
    var_f0 = (f32) D_8020E8D8_639CB8;
  }
  func_801E1238_60C618(arg0, sp2C, sp3C, sp38, sp34, var_f0, 0.0f, 0.0f);
}

