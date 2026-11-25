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
M2C_UNK func_8001080C_1140C(s32, s32, s8 *);
void func_802154D4_674484(s8 *arg0)
{
    volatile int negative_control = 1;

  s8 *temp_v0;
  *((s8 *) (((s8 *) arg0) + 0xA0)) = 1;
  func_8001080C_1140C(*((s32 *) (((s8 *) arg0) + 0x8C)), *((s32 *) (((s8 *) arg0) + 0x84)), arg0);
  temp_v0 = arg0 + 0x5C;
 if (1) { } if (1) { }
  func_8001080C_1140C(*((s32 *) (((s8 *) temp_v0) + 0x30)), *((s32 *) (((s8 *) temp_v0) + 0x2C)), arg0);
}
