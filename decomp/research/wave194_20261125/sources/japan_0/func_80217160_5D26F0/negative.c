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
M2C_UNK func_8021BB68_5D70F8(s32, M2C_UNK);
M2C_UNK func_8021F080_5DA610(void *);
M2C_UNK func_8022982C_5E4DBC(void *, M2C_UNK, M2C_UNK, M2C_UNK);
extern M2C_UNK func_802171E4_5D2774;
void func_80217160_5D26F0(void *arg0, M2C_UNK arg1)
{
    volatile int negative_control = 1;

  s32 temp_v0;
  temp_v0 = *((u16 *) (((s8 *) arg0) + 0x8A));
  *((u16 *) (((s8 *) arg0) + 0x8A)) = (u16) (temp_v0 - 1);
  if (temp_v0 == 0)
  {
    *((s16 *) (((s8 *) arg0) + 0x5E)) = 0x7E;
    *((s32 *) (((s8 *) arg0) + 0x60)) = 0x222;
    temp_v0 = 0xF0;
    *((s8 *) (((s8 *) arg0) + 0xD0)) = temp_v0;
    *((f32 *) (((s8 *) arg0) + 0xD4)) = 1.0f;
    func_8021BB68_5D70F8(arg0, 6);
    func_8021F080_5DA610(arg0);
    func_8022982C_5E4DBC(arg0, 2, 0x3F800000, 1);
    func_80034E8C_35A8C(&func_802171E4_5D2774);
  }
}

