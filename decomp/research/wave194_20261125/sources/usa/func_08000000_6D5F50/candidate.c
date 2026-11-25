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
extern f32 D_08003ECC_6D9E1C;
void func_08000000_6D5F50(void *arg0)
{
  f32 *new_var;
  s8 *new_var2;
  new_var2 = (s8 *) (*((void **) (((s8 *) arg0) + 0x18)));
  new_var = (f32 *) (new_var2 + 0xC);
  if (D_08003ECC_6D9E1C < (*new_var))
  {
    *((s32 *) (((s8 *) arg0) + 0x68)) = (s32) ((*((s32 *) (((s8 *) arg0) + 0x68))) | 2);
  }
}

