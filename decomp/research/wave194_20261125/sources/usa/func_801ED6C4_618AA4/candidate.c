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
M2C_UNK func_8003521C_35E1C(M2C_UNK *);
extern f32 D_8020E214_6395F4;
extern void *D_8020EED0_63A2B0;
extern M2C_UNK func_801ED73C_618B1C;
void func_801ED6C4_618AA4(void *arg0, M2C_UNK arg1)
{
  s32 temp_v0;
  if ((*((u8 *) (((s8 *) D_8020EED0_63A2B0) + 0x2C1))) == 0)
  {
    temp_v0 = *((s32 *) (((s8 *) arg0) + 0x7C));
    *((s32 *) (((s8 *) arg0) + 0x7C)) = (s32) (temp_v0 - 1);
    if (temp_v0 <= 0)
    {
      *((f32 *) (((s8 *) arg0) + 0x90)) = 0.5f;
      *((f32 *) (((s8 *) arg0) + 0x94)) = (f32) D_8020E214_6395F4;
      *((s32 *) (((s8 *) arg0) + 0x7C)) = 0xB4;
      *((s32 *) (((s8 *) arg0) + 0x80)) = 0x64;
      func_8003521C_35E1C(&func_801ED73C_618B1C);
    }
  }
}

