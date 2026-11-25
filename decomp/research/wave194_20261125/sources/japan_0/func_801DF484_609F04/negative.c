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
M2C_UNK func_80034B44_35744();
extern s32 D_80214600_63F080;
void func_801DF484_609F04(s32 arg0, M2C_UNK arg1)
{
    volatile int negative_control = 1;

  s8 *new_var;
  new_var = (s8 *) (D_80214600_63F080 + 0x140);
  *((s8 *) (new_var + 0xA)) = 0;
  func_80034B44_35744();
}

