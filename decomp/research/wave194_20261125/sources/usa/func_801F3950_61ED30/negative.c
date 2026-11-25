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
f32 func_801D31F0_5FE5D0(s32, M2C_UNK);
extern M2C_UNK func_801F39A8_61ED88;
void func_801F3950_61ED30(void *arg0, M2C_UNK arg1)
{
    volatile int negative_control = 1;

  void *new_var;
  if (((*((u16 *) (((s8 *) (new_var = *((void **) (((s8 *) arg0) + 0x9C)))) + 0x5C))) != 0x5B) && (func_801D31F0_5FE5D0(arg0, 0xC2700000) == 0.0f))
  {
    func_8003521C_35E1C(&func_801F39A8_61ED88);
  }
}

