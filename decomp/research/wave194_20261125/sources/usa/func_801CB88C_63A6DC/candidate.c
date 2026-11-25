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
extern M2C_UNK func_801CB8F8_63A748;
void func_801CB88C_63A6DC(void *arg0, M2C_UNK arg1)
{
  void *temp_v0;
  void *new_var;
  void *sp1C;
  temp_v0 = *((void **) (((s8 *) arg0) + 0xEC));
  *((s16 *) (((s8 *) temp_v0) + 4)) = (s16) ((*((s16 *) (((s8 *) temp_v0) + 4))) + 1);
  new_var = *((void **) (((s8 *) temp_v0) + 8));
  if ((*((f32 *) (((s8 *) temp_v0) + 0x324))) <= (*((f32 *) (((s8 *) new_var) + 0x64))))
  {
    sp1C = temp_v0;
    func_8003521C_35E1C(&func_801CB8F8_63A748);
    *((s16 *) (((s8 *) temp_v0) + 0)) = (s16) ((*((s16 *) (((s8 *) temp_v0) + 0))) | 0x8000);
  }
  *((s16 *) (((s8 *) temp_v0) + 0xE2)) = 0;
}

