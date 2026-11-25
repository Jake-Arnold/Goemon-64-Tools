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
void func_08000948_717DE8(void *arg0, s8 arg1, s8 arg2, s8 arg3, s8 arg4)
{
  *((s8 *) (((s8 *) arg0) + 0xD8)) = arg1;
  *((s8 *) (((s8 *) arg0) + 0xD9)) = arg2;
  *((s8 *) (((s8 *) arg0) + 0xDA)) = arg3;
  *((s8 *) (((s8 *) arg0) + 0xDB)) = arg4;
  *((s8 *) (((s8 *) arg0) + 0xE6)) = 0x1E;
  *((s8 *) (((s8 *) arg0) + 0xE7)) = 0x1E;
}

