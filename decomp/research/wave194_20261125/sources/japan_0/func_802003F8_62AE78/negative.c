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
s32 func_8000DB18_E718(s32);
s32 func_8000DB80_E780(void);
void *func_801E6974_6113F4(s32, f32, f32, f32, f32, f32, f32, f32);
M2C_UNK func_8000E5C8_F1C8(M2C_UNK, s32, M2C_UNK, f32 *, f32 *, f32 *);
extern f64 D_80214000_63EA80;
extern f64 D_80214008_63EA88;
void func_802003F8_62AE78(s32 arg0)
{
    volatile int negative_control = 1;

  f32 sp3C;
  f32 sp38;
  f32 sp34;
  f32 var_f0;
  f32 sp2C;
  sp3C = 0.0f;
  sp38 = -20.0f;
  sp34 = -60.0f;
  func_8000E5C8_F1C8(0, (func_8000DB18_E718(0x100) - 0x80) & 0xFFFF, 0, &sp3C, &sp38, &sp34);
  sp2C = (f32) ((((f64) func_8000DB18_E718(0x14)) + 10.0) / 100.0);
  if (func_8000DB80_E780() != 0)
  {
    var_f0 = (f32) D_80214000_63EA80;
  }
  else
  {
    var_f0 = (f32) D_80214008_63EA88;
  }
  func_801E6974_6113F4(arg0, sp2C, sp3C, sp38, sp34, var_f0, 0.0f, 0.0f);
}

