typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
f32 func_801CD96C_63C7BC(void *, s32);
extern f64 D_801EF060_65DEB0;

void func_801D3198_641FE8(void *arg0, void *arg1) {
    s16 temp_v0;

    temp_v0 = M2C_FIELD(arg0, s16 *, 0xA8);
    if (((temp_v0 == 0) || (M2C_FIELD(arg0, s16 *, 0xA8) = --temp_v0, (temp_v0 == 0))) && ((f64) func_801CD96C_63C7BC(arg0, 0) < D_801EF060_65DEB0)) {
        M2C_FIELD(arg0, s8 *, 0x9D) = 1;
        M2C_FIELD(arg1, f32 *, 0x28) = (f32) ((f64) M2C_FIELD(arg1, f32 *, 0x28) + 0.5);
    }
}
