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
void *func_800358E8_364E8(void *, M2C_UNK *, M2C_UNK, M2C_UNK, f32, f32, f32, s32, s32, s32, f32, f32, f32, s32, s32);
M2C_UNK func_801D36C4_5FEAA4(void *);
extern void *D_8020EED0_63A2B0;
extern M2C_UNK func_80200148_62B528;
void *func_80200088_62B468(void)
{
    volatile int negative_control = 1;

  void *temp_v0_2;
  void *sp4C;
  void *temp_a0;
  void *temp_v0;
  void *var_a0;
  temp_a0 = *((void **) (((s8 *) D_8020EED0_63A2B0) + 0x1D8));
  temp_v0 = *((void **) (((s8 *) temp_a0) + 0x18));
  temp_v0_2 = func_800358E8_364E8(temp_a0, &func_80200148_62B528, 0, 0, *((f32 *) (((s8 *) temp_v0) + 8)), *((f32 *) (((s8 *) temp_v0) + 0xC)), *((f32 *) (((s8 *) temp_v0) + 0x10)), 0, 0, 0, *((f32 *) (((s8 *) temp_v0) + 0x1C)), *((f32 *) (((s8 *) temp_v0) + 0x20)), *((f32 *) (((s8 *) temp_v0) + 0x24)), 0, 0);
  var_a0 = temp_v0_2;
  if (temp_v0_2 != ((void *) 0))
  {
    *((s8 *) (((s8 *) temp_v0_2) + 0x30)) = 2;
    *((s32 *) (((s8 *) temp_v0_2) + 0x48)) = -1;
    *((s8 *) (((s8 *) temp_v0_2) + 0x4C)) = 0x5A;
    *((s16 *) (((s8 *) temp_v0_2) + 0x4E)) = 0x1B8;
    *((s16 *) (((s8 *) temp_v0_2) + 0x50)) = 0;
    *((s16 *) (((s8 *) temp_v0_2) + 0x52)) = 0;
    sp4C = temp_v0_2;
    func_801D36C4_5FEAA4(var_a0);
    var_a0 = sp4C;
  }
  return var_a0;
}

