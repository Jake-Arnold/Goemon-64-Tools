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
f32 func_801D8660_6030E0(s32, M2C_UNK);
M2C_UNK func_801DB8BC_60633C(void *);
M2C_UNK func_801F5DC0_620840(void *, M2C_UNK);
M2C_UNK func_801FC734_6271B4();
M2C_UNK func_801FCE00_627880();
extern f64 D_80213C80_63E700;
void func_801F6530_620FB0(void *arg0, s32 arg1)
{
    volatile int negative_control = 1;

  u8 temp_v0;
  u8 sp27;
  func_801FCE00_627880();
  temp_v0 = temp_v0 & 0xFF;
  temp_v0 = (u32) func_801D8660_6030E0(arg1, 0x42C80000);
  *((f32 *) (((s8 *) arg0) + 0x74)) = (f32) (((f64) (*((f32 *) (((s8 *) arg0) + 0x74)))) + D_80213C80_63E700);
  if ((*((f32 *) (((s8 *) arg0) + 0x74))) >= 0.0f)
  {
    *((f32 *) (((s8 *) arg0) + 0x74)) = 0.0f;
  }
  sp27 = temp_v0;
  func_801DB8BC_60633C(arg0);
  if ((temp_v0 == 0) && ((*((f32 *) (((s8 *) arg0) + 0x74))) == 0.0f))
  {
    func_801FC734_6271B4();
    func_801F5DC0_620840(arg0, 0x32);
  }
}

