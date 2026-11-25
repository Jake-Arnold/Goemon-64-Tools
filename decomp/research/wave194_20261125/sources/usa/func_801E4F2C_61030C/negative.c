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
M2C_UNK func_801D31CC_5FE5AC(s32, M2C_UNK *);
M2C_UNK func_801D34D0_5FE8B0(void *, M2C_UNK *, M2C_UNK, M2C_UNK);
extern M2C_UNK D_8020B094_636474;
extern M2C_UNK D_8020B1D0_6365B0;
extern M2C_UNK func_801E4FB0_610390;
void func_801E4F2C_61030C(s32 arg0, void *arg1)
{
    volatile int negative_control = 1;

  *((s16 *) (((s8 *) arg1) + 0x14)) = 0;
  *((s16 *) (((s8 *) arg1) + 0x16)) = 0;
  *((f32 *) (((s8 *) arg1) + 8)) = 0.0f;
  *((s16 *) (((s8 *) arg1) + 0x18)) = 0;
  *((f32 *) (((s8 *) arg1) + 0xC)) = -135.0f;
  *((f32 *) (((s8 *) arg1) + 0x10)) = -500.0f;
  func_801D34D0_5FE8B0(arg1, &D_8020B094_636474, 0, 1);
  func_801D31CC_5FE5AC(arg0, &D_8020B1D0_6365B0);
  func_8003521C_35E1C(&func_801E4FB0_610390);
}

