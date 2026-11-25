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
s32 func_80014480_15080(s32, M2C_UNK);
s32 func_80034A78_35678(s32, M2C_UNK *, M2C_UNK);
extern s32 g_system_ptr;
extern void *D_80214600_63F080;
extern s32 D_80214660_63F0E0;
extern M2C_UNK func_801D179C_5FC21C;
extern M2C_UNK func_801F4A10_61F490;
extern M2C_UNK func_801FC37C_626DFC;
s32 func_801FC7B8_627238(void)
{
  char pad;
  void *sp20;
  s32 temp_v0;
  sp20 = D_80214600_63F080;
  D_80214660_63F0E0 = 0;
  temp_v0 = func_80014480_15080(g_system_ptr + 0xC7FA4, 0x10);
  if (temp_v0 == 0)
  {
    return 0;
  }
  D_80214660_63F0E0 = temp_v0;
  *((s32 *) (((s8 *) D_80214600_63F080) + 0x1D0)) = func_80034A78_35678(*((s32 *) (((s8 *) D_80214600_63F080) + 0x1C4)), &func_801FC37C_626DFC, 0);
  *((s32 *) (((s8 *) D_80214600_63F080) + 0x1D8)) = func_80034A78_35678(*((s32 *) (((s8 *) D_80214600_63F080) + 0x1C4)), &func_801F4A10_61F490, 0);
  *((s32 *) (((s8 *) D_80214600_63F080) + 0x1D4)) = func_80034A78_35678(*((s32 *) (((s8 *) D_80214600_63F080) + 0x1BC)), &func_801D179C_5FC21C, 0);
  *((s32 *) (((s8 *) sp20) + 0x60)) = 0x7D0;
  return *((s32 *) (((s8 *) D_80214600_63F080) + 0x1D8));
}

