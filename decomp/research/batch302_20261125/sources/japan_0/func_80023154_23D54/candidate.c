typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_800237A4_243A4(s32);                   /* extern */
s32 osPfsFileState(void *, s32, void *);            /* extern */
extern void *D_8016E664_16F264;

s32 func_80023154_23D54(void) {
    s32 sp1C;
    s32 temp_a1;
    s32 temp_v0;

    temp_a1 = M2C_FIELD(D_8016E664_16F264, s32 *, 0x3F0);
    temp_v0 = osPfsFileState(D_8016E664_16F264, temp_a1, ((s8 *)D_8016E664_16F264) + (temp_a1 << 5) + 0x1B0);
    sp1C = temp_v0;
    func_800237A4_243A4(temp_v0);
    M2C_FIELD(D_8016E664_16F264, s32 *, 0x3FC) = sp1C;
    return M2C_FIELD(D_8016E664_16F264, s32 *, 0x3FC);
}
