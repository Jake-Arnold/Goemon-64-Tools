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
M2C_UNK func_801E8858_5A4768(void *, M2C_UNK);
M2C_UNK func_801EAE88_5A6D98();
extern f32 D_8020B88C_5C779C;
extern f32 D_8020B890_5C77A0;
extern M2C_UNK func_801EADBC_5A6CCC;
void func_801EAD38_5A6C48(void *arg0, void *arg1)
{
  f32 temp_f2;
  func_801EAE88_5A6D98();
  func_801E8858_5A4768(arg1, 0xA);
  *((f32 *) (((s8 *) arg1) + 0x1C)) = (f32) ((*((f32 *) (((s8 *) arg1) + 0x1C))) + D_8020B88C_5C779C);
  temp_f2 = *((f32 *) (((s8 *) arg1) + 0x1C));
  *((f32 *) (((s8 *) arg1) + 0x24)) = temp_f2;
  *((f32 *) (((s8 *) arg1) + 0x20)) = temp_f2;
  if (D_8020B890_5C77A0 <= (*((f32 *) (((s8 *) arg1) + 0x1C))))
  {
    *((s8 *) (((s8 *) arg0) + 0x60)) = 2;
    func_8003521C_35E1C(&func_801EADBC_5A6CCC);
  }
}

