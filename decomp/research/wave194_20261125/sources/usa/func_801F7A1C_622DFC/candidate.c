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
M2C_UNK func_8000DD04_E904(s32);
M2C_UNK func_80034ED4_35AD4();
M2C_UNK func_80038BC8_397C8(M2C_UNK);
s32 func_801D365C_5FEA3C(s8 *);
M2C_UNK func_801D36C4_5FEAA4(s8 *);
extern s8 *D_8020EED0_63A2B0;
void func_801F7A1C_622DFC(s8 *arg0)
{
  s8 *sp24;
  s8 *temp_v0;
  s8 *sp1C;
  sp1C = D_8020EED0_63A2B0 + 0x140;
  temp_v0 = *((s8 **) (((s8 *) D_8020EED0_63A2B0) + 0x1D8));
  sp24 = temp_v0;
  func_8000DD04_E904(*((s32 *) (((s8 *) temp_v0) + 0x18)));
  if (((func_801D365C_5FEA3C(arg0) == (*((s32 *) (((s8 *) D_8020EED0_63A2B0) + 0x1CC)))) && ((*((u8 *) (((s8 *) sp1C) + 0xE))) == 0)) && ((*((u8 *) (((s8 *) D_8020EED0_63A2B0) + 0x2C5))) == 0))
  {
    *((s8 *) (((s8 *) arg0) + 0x30)) = 0;
    *((s32 *) (((s8 *) arg0) + 0x48)) = 0;
    func_80038BC8_397C8(0x24A);
  }
  func_801D36C4_5FEAA4(arg0);
  temp_v0 = *((s8 **) (((s8 *) D_8020EED0_63A2B0) + 0x1D8));
  if ((*((s32 *) (((s8 *) sp24) + 0xD8))) != 4)
  {
    func_80034ED4_35AD4();
  }
}

