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
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);
f32 func_801D8910_603390(s32, M2C_UNK);
extern M2C_UNK func_801F90D8_623B58;
void func_801F9080_623B00(void *arg0, M2C_UNK arg1)
{
    volatile int negative_control = 1;

  void *new_var;
  if (((*((u16 *) (((s8 *) (new_var = *((void **) (((s8 *) arg0) + 0x9C)))) + 0x5C))) != 0x5B) && (func_801D8910_603390(arg0, 0xC2700000) == 0.0f))
  {
    func_80034E8C_35A8C(&func_801F90D8_623B58);
  }
}

