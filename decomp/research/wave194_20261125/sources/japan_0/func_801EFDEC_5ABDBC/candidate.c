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
M2C_UNK func_801ED918_5A98E8(void *, M2C_UNK);
M2C_UNK func_801EFF3C_5ABF0C();
extern f32 D_802106AC_5CC67C;
extern f32 D_802106B0_5CC680;
extern M2C_UNK func_801EFE70_5ABE40;
void func_801EFDEC_5ABDBC(void *arg0, void *arg1)
{
  f32 temp_f2;
  func_801EFF3C_5ABF0C();
  func_801ED918_5A98E8(arg1, 0xA);
  *((f32 *) (((s8 *) arg1) + 0x1C)) = (f32) ((*((f32 *) (((s8 *) arg1) + 0x1C))) + D_802106AC_5CC67C);
  temp_f2 = *((f32 *) (((s8 *) arg1) + 0x1C));
  *((f32 *) (((s8 *) arg1) + 0x24)) = temp_f2;
  *((f32 *) (((s8 *) arg1) + 0x20)) = temp_f2;
  if (D_802106B0_5CC680 <= (*((f32 *) (((s8 *) arg1) + 0x1C))))
  {
    *((s8 *) (((s8 *) arg0) + 0x60)) = 2;
    func_80034E8C_35A8C(&func_801EFE70_5ABE40);
  }
}

