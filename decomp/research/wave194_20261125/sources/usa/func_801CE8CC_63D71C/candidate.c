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
extern f64 D_801EEE48_65DC98;
void func_801CE8CC_63D71C(void *arg0, M2C_UNK arg1)
{
  s32 temp_f16;
  temp_f16 = (s32) (((f64) (*((s32 *) (((s8 *) arg0) + 0xB4)))) + D_801EEE48_65DC98);
  if (temp_f16 >= 0x2328)
  {
    *((s8 *) (((s8 *) arg0) + 0x9D)) = 2;
    *((s8 *) (((s8 *) arg0) + 0x9F)) = (s8) ((*((s8 *) (((s8 *) arg0) + 0x9F))) & 0xFFFE);
    *((s32 *) (((s8 *) arg0) + 0xB0)) = 0x8CA0;
  }
  *((s32 *) (((s8 *) arg0) + 0xB4)) = temp_f16;
}

