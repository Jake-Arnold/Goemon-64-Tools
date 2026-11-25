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
M2C_UNK func_801FBF18_5B7EE8();
void func_801FBF50_5B7F20(void *arg0)
{
    volatile int negative_control = 1;

  func_801FBF18_5B7EE8();
  *((f32 *) (((s8 *) (*((void **) (((s8 *) arg0) + 0x5C)))) + 0x50)) = 0.f;
  *((s16 *) (((s8 *) (*((void **) (((s8 *) arg0) + 0x5C)))) + 0)) = 0;
  *((f32 *) (((s8 *) arg0) + 0xE4)) = 0.0f;
  *((f32 *) (((s8 *) arg0) + 0xE8)) = 0.0f;
}

