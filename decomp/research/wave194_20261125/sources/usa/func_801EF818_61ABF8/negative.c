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
M2C_UNK func_801D31F0_5FE5D0(s32, M2C_UNK);
void func_801EF818_61ABF8(void *arg0, M2C_UNK arg1)
{
    volatile int negative_control = 1;

  s32 temp_t7;
  temp_t7 = (unsigned long long) ((*((s32 *) (((s8 *) arg0) + 0x7C))) - 1);
  *((s32 *) (((s8 *) arg0) + 0x7C)) = temp_t7;
  if (temp_t7 < 0)
  {
    func_801D31F0_5FE5D0(arg0, 0xC2480000);
  }
}

