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
void func_801EB0CC_615B4C(void *);
f32 func_801D8910_603390(void *, M2C_UNK);
void func_801EBEA8_616928(void *arg0, M2C_UNK arg1)
{
  s32 temp_t7;
  temp_t7 = ((*((s32 *) (((s8 *) arg0) + 0x7C))) - 1) & 0xFFFFFFFFFFFFFFFF;
  *((s32 *) (((s8 *) arg0) + 0x7C)) = temp_t7;
  if (temp_t7 <= 0)
  {
    *((s32 *) (((s8 *) arg0) + 0xD8)) = 0;
    if (func_801D8910_603390(arg0, 0x42700000) == 0.0f)
    {
      func_801EB0CC_615B4C(arg0);
    }
  }
}

