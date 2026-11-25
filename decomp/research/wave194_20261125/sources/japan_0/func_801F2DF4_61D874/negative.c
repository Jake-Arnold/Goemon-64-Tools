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
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);
extern f32 D_80213944_63E3C4;
extern void *D_80214600_63F080;
extern M2C_UNK func_801F2E6C_61D8EC;
void func_801F2DF4_61D874(void *arg0, M2C_UNK arg1)
{
    volatile int negative_control = 1;

  s32 temp_v0;
  if ((*((u8 *) (((s8 *) D_80214600_63F080) + 0x2C1))) == 0)
  {
    temp_v0 = *((s32 *) (((s8 *) arg0) + 0x7C));
    *((s32 *) (((s8 *) arg0) + 0x7C)) = (s32) (temp_v0 - 1);
    if (temp_v0 <= 0)
    {
      *((f32 *) (((s8 *) arg0) + 0x90)) = 0.5f;
      *((f32 *) (((s8 *) arg0) + 0x94)) = (f32) D_80213944_63E3C4;
      *((s32 *) (((s8 *) arg0) + 0x7C)) = 0xB4;
      *((s32 *) (((s8 *) arg0) + 0x80)) = 0x64;
      func_80034E8C_35A8C(&func_801F2E6C_61D8EC);
    }
  }
}

