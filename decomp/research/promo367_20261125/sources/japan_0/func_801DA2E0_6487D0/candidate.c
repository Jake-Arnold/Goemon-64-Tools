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
void func_801DA2E0_6487D0(void *arg0, M2C_UNK arg1)
{
  s16 temp_v1;
  s32 temp_v0;
  s32 temp_v1_2;
 do { temp_v0 = *((s32 *) (((s8 *) arg0) + 0xa0)); temp_v1 = (*((s16 *) (((s8 *) arg0) + 0xa8))) - 1; *((s16 *) (((s8 *) arg0) + 0xa8)) = temp_v1; *((f32 *) (((s8 *) arg0) + 0x60)) = (f32) ((*((f32 *) (((s8 *) arg0) + 0x60))) + (((f32) temp_v0) / 1000.0f)); } while (0);
  if (temp_v1 == 0)
  {
    *((s8 *) (((s8 *) arg0) + 0x9c)) = 1;
    temp_v1_2 = -(*((s32 *) (((s8 *) arg0) + 0xa4)));
    *((s32 *) (((s8 *) arg0) + 0xa4)) = temp_v1_2;
    *((s32 *) (((s8 *) arg0) + 0xa0)) = (s32) (temp_v0 + temp_v1_2);
  }
}
