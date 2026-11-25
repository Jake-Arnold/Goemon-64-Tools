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
extern void *D_801C1728_1C2328;
extern s32 D_801C172C_1C232C;
int func_8003CB8C_3D78C(void)
{
  u8 temp_a0;
  ;
  switch (*((u8 *) (((s8 *) D_801C1728_1C2328) + 0x70)))
  {
    case 0:
      *((u8 *) (((s8 *) D_801C1728_1C2328) + 0x70)) = (u8) ((*((u8 *) (((s8 *) D_801C1728_1C2328) + 0x70))) + 1);
      return;

    case 1:
      *((u8 *) (((s8 *) D_801C1728_1C2328) + 0x70)) = (u8) ((*((u8 *) (((s8 *) D_801C1728_1C2328) + 0x70))) + 1);
      *((s32 *) (((s8 *) D_801C1728_1C2328) + 0x78)) = (s32) D_801C172C_1C232C;
      D_801C172C_1C232C = *((s32 *) (((s8 *) D_801C1728_1C2328) + 0x74));
      return;

    case 2:
      *((u8 *) (((s8 *) D_801C1728_1C2328) + 0x70)) = (u8) ((*((u8 *) (((s8 *) D_801C1728_1C2328) + 0x70))) - 1);
      D_801C172C_1C232C = *((s32 *) (((s8 *) D_801C1728_1C2328) + 0x78));
      return;

  }

}

