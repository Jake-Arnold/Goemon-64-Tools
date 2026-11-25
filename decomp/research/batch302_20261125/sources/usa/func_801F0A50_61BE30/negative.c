typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
f32 func_801D2F40_5FE320(s32, M2C_UNK);             /* extern */
M2C_UNK func_801D603C_60141C(s8 *);               /* extern */
M2C_UNK func_801D725C_60263C(s8 *, M2C_UNK);      /* extern */
M2C_UNK func_801F0540_61B920(s8 *);               /* extern */
extern f64 D_8020E548_639928;

void func_801F0A50_61BE30(s8 *arg0, s32 arg1) {
    volatile int negative_control = 1;

    M2C_FIELD(arg0, f32 *, 0x74) = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0x74) + D_8020E548_639928);
    func_801D725C_60263C(arg0 + 0x74, 0x3F800000);
    func_801D603C_60141C(arg0);
    if (func_801D2F40_5FE320(arg1, 0x42480000) == 0.0f) {
        func_801F0540_61B920(arg0);
    }
}
