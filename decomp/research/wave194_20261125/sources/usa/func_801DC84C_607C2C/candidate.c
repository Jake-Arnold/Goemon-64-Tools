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
M2C_UNK func_8003521C_35E1C(M2C_UNK *);
M2C_UNK func_801D614C_60152C();
extern M2C_UNK func_801DC890_607C70;
void func_801DC84C_607C2C(void *arg0, M2C_UNK arg1)
{
  int temp_v0;
 do { func_801D614C_60152C(); temp_v0 = *((s32 *) (((s8 *) arg0) + 0x7C)); *((s32 *) (((s8 *) arg0) + 0x7C)) = (s32) ((*((s32 *) (((s8 *) arg0) + 0x7C))) - 1); } while (0);
  if (temp_v0 <= 0)
  {
    func_8003521C_35E1C(&func_801DC890_607C70);
  }
}
