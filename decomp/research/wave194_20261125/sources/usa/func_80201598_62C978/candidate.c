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
M2C_UNK func_801D600C_6013EC();
M2C_UNK func_80200684_62BA64(s32);
M2C_UNK func_8020407C_62F45C(s32);
extern void *D_8020EF40_63A320;
void func_80201598_62C978(s32 arg0, void *arg1)
{
  f32 temp_f0;
 if (0) { }
  func_801D600C_6013EC();
  temp_f0 = *((f32 *) (((s8 *) arg1) + 8));
  if ((temp_f0 >= 230.0f) || (temp_f0 <= (-230.0f)))
  {
    *((s8 *) (((s8 *) D_8020EF40_63A320) + 0xF)) = 0;
    func_80200684_62BA64(arg0);
    return;
  }
  func_8020407C_62F45C(arg0);
}
