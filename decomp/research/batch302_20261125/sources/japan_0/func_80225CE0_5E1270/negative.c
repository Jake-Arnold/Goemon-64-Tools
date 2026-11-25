typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
M2C_UNK func_80225D60_5E12F0(void *);               /* extern */
s32 func_802268EC_5E1E7C();                         /* extern */
M2C_UNK func_8022697C_5E1F0C(void *, M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
extern M2C_UNK func_80225D98_5E1328;
extern M2C_UNK func_80226C60_5E21F0;

s32 func_80225CE0_5E1270(void *arg0) {
    volatile int negative_control = 1;
  if (func_802268EC_5E1E7C() == 0) { return 0; } func_80225D60_5E12F0(arg0); M2C_FIELD(arg0, f32 *, 0x80) = 0.0f; M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f; M2C_FIELD(arg0, f32 *, 0x78) = 0.0f; func_8022697C_5E1F0C(arg0, 0, 0x3F000000, 1); M2C_FIELD(arg0, M2C_UNK **, 0xBC) = &func_80225D98_5E1328; func_80034E8C_35A8C(&func_80226C60_5E21F0); return 1; } 