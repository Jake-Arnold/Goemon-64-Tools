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
void func_800115B8_121B8(s32 arg0, s32 arg1, s32 arg2)
{
  void *temp_v0;
  temp_v0 = arg0 + 0x5C;
  if (arg0 != 0)
  {
 do { *((s32 *) (((s8 *) temp_v0) + 8)) = (s32) ((*((s32 *) (((s8 *) temp_v0) + 8))) + arg1); *((s32 *) (((s8 *) temp_v0) + 0xC)) = (s32) ((*((s32 *) (((s8 *) temp_v0) + 0xC))) + arg2); } while (0);
  }
}
