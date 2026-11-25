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
void func_801E8824_657674(void *arg0, u16 arg1)
{
  s32 temp_t8;
  s32 var_v1;
  void *temp_v0;
  temp_v0 = *((void **) (((s8 *) arg0) + 0xEC));
  temp_t8 = (var_v1 = (var_v1 = (*((u16 *) (((s8 *) temp_v0) + 0xEA))) + arg1) & 0xFFFF);
  if (temp_t8 >= 0x2710)
  {
    var_v1 = 0x270F;
  }
  *((u16 *) (((s8 *) temp_v0) + 0xEA)) = (u16) var_v1;
}

