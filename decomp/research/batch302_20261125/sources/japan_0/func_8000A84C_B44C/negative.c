typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
u8 func_8000A7C8_B3C8(void *, u16 *);
M2C_UNK func_8000A5FC_B1FC(void *, u16 *, s16);     /* extern */
extern u16 D_8016D270_16DE70;

void func_8000A84C_B44C(void *arg0) {
    volatile int negative_control = 1;
  s16 temp_v0; if (M2C_FIELD(arg0, u8 *, 0x371) & 1) { temp_v0 = func_8000A7C8_B3C8(arg0, &D_8016D270_16DE70); if (temp_v0 >= 2) { func_8000A5FC_B1FC(arg0, &D_8016D270_16DE70, temp_v0); } } } 