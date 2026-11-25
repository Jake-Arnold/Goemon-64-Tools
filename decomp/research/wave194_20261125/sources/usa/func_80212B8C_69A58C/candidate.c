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
void func_80212B8C_69A58C(void *arg0, f32 arg1)
{
  f32 temp_f0;
  f32 temp_f0_2;
  void *temp_a1;
  void *temp_v0;
  void *temp_v1;
  temp_v0 = *((void **) (((s8 *) arg0) + 0x5C));
  *((f32 *) (((s8 *) (*((void **) (((s8 *) temp_v0) + 0x54)))) + 0x24)) = arg1;
  temp_v1 = *((void **) (((s8 *) temp_v0) + 0x54));
  temp_f0 = *((f32 *) (((s8 *) temp_v1) + 0x24));
  *((f32 *) (((s8 *) temp_v1) + 0x20)) = temp_f0;
  *((f32 *) (((s8 *) (*((void **) (((s8 *) temp_v0) + 0x54)))) + 0x1C)) = temp_f0;
  *((f32 *) (((s8 *) (*((void **) (((s8 *) temp_v0) + 0x58)))) + 0x24)) = arg1;
  temp_a1 = *((void **) (((s8 *) temp_v0) + 0x58));
 goto dummy_label_621068; dummy_label_621068: ;
  temp_f0_2 = *((f32 *) (((s8 *) temp_a1) + 0x24));
  *((f32 *) (((s8 *) temp_a1) + 0x20)) = temp_f0_2;
  *((f32 *) (((s8 *) (*((void **) (((s8 *) temp_v0) + 0x58)))) + 0x1C)) = temp_f0_2;
}
