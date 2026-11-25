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
M2C_UNK func_8021DB18_5D90A8(void *, M2C_UNK, M2C_UNK, M2C_UNK);
M2C_UNK func_8021EBE0_5DA170(void *, M2C_UNK, M2C_UNK);
M2C_UNK func_802213C4_5DC954();
void func_80226800_5E1D90(void *arg0)
{
  void *temp_v0;
  temp_v0 = *((void **) (((s8 *) arg0) + 0x18));
  *((s32 *) (((s8 *) arg0) + 0x60)) = 0x12800761;
  *((s32 *) (((s8 *) arg0) + 0x64)) = 0x20;
  *((s16 *) (((s8 *) arg0) + 0xA4)) = (s16) (*((s32 *) (((s8 *) arg0) + 0xD4)));
  *((s8 *) (((s8 *) arg0) + 0x4C)) = 2;
  *((s32 *) (((s8 *) arg0) + 0x68)) = 0x400;
  if ((((*((f32 *) (((s8 *) temp_v0) + 8))) != 0.0f) || ((*((f32 *) (((s8 *) temp_v0) + 0xC))) != 0.0f)) || ((*((f32 *) (((s8 *) temp_v0) + 0x10))) != 0.0f))
  {
    func_802213C4_5DC954();
  }
  func_8021EBE0_5DA170(arg0, 5, 0);
  func_8021DB18_5D90A8(arg0, 0x3E8, 0x64, 0);
}

