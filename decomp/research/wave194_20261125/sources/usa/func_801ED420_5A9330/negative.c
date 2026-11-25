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
M2C_UNK func_801DC554_598464(M2C_UNK, s8 *, M2C_UNK *, M2C_UNK, s32, s32, s32, s32, s32, s32);
M2C_UNK func_801EE330_5AA240(u8 *, M2C_UNK, M2C_UNK);
extern M2C_UNK D_80204CA8_5C0BB8;
extern f32 D_8020BAA0_5C79B0;
void func_801ED420_5A9330(s8 *arg0)
{
    volatile int negative_control = 1;

  f32 temp_f0;
  f32 temp_f20;
  s32 var_s2;
  u8 *var_s1;
  s8 *var_s0;
  var_s0 = *((s8 **) (((s8 *) arg0) + 0x18));
 temp_f20 = D_8020BAA0_5C79B0; var_s2 = 0; var_s1 = arg0 + 0xA0; do { if ((*var_s1) != 0) {
      *((f32 *) (((s8 *) var_s0) + 0x1C)) = (f32) ((*((f32 *) (((s8 *) var_s0) + 0x1C))) + temp_f20);
      temp_f0 = *((f32 *) (((s8 *) var_s0) + 0x1C));
      *((f32 *) (((s8 *) var_s0) + 0x24)) = temp_f0;
      *((f32 *) (((s8 *) var_s0) + 0x20)) = temp_f0;
      func_801EE330_5AA240(var_s1, 0x1A, 0);
      func_801DC554_598464(0, var_s0 + 0x80, &D_80204CA8_5C0BB8, 0, 0, 0, 0xF5, 0xD, 0, (s32) (*var_s1));
    }
    var_s2 += 1;
    var_s1 += 1;
    var_s0 = *((s8 **) (((s8 *) var_s0) + 0));
  }
  while (var_s2 != 4);
}
