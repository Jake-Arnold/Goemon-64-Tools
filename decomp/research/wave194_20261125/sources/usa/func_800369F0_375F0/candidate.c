typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80036A28_37628();                      /* extern */
extern M2C_UNK D_3B014;
extern s32 D_8015C5C8_15D1C8;

void func_800369F0_375F0(void) {
    func_80036A28_37628();
    M2C_FIELD(*(s32 *)((s8 *)&D_3B014 + (D_8015C5C8_15D1C8)), s8 *, 0x10) = 0;
}
