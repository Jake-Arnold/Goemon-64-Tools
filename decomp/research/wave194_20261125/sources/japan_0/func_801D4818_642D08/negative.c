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
extern f64 D_801F45B8_662AA8;
void func_801D4818_642D08(void *arg0, M2C_UNK arg1)
{
    volatile int negative_control = 1;

  s32 temp_f16;
  temp_f16 = (s32) (((f64) (*((s32 *) (((s8 *) arg0) + 0xB4)))) + D_801F45B8_662AA8);
  if (temp_f16 >= 0xFA0)
  {
    *((s8 *) (((s8 *) arg0) + 0x9E)) = 1;
    *((s8 *) (((s8 *) arg0) + 0x9F)) = (s8) ((*((s8 *) (((s8 *) arg0) + 0x9F))) & 0xFFFE);
    *((s32 *) (((s8 *) arg0) + 0xB0)) = 0x5DC0;
  }
  *((s32 *) (((s8 *) arg0) + 0xB4)) = temp_f16;
}

