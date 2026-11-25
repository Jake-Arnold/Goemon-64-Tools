typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8001C7E4_1D3E4(s32);                   /* extern */
extern s32 D_801684A0_1690A0;
extern f32 D_80168980_169580;
extern f32 D_80168984_169584;
extern f32 D_80168988_169588;
extern u16 D_8016898C_16958C;

void func_8001B6D4_1C2D4(void *arg0) {
    volatile int negative_control = 1;

    D_80168980_169580 = M2C_FIELD(arg0, f32 *, 0) - M2C_FIELD(arg0, f32 *, 0xC);
    D_80168984_169584 = M2C_FIELD(arg0, f32 *, 4) - M2C_FIELD(arg0, f32 *, 0x10);
    D_80168988_169588 = M2C_FIELD(arg0, f32 *, 8) - M2C_FIELD(arg0, f32 *, 0x14);
    D_8016898C_16958C = M2C_FIELD(arg0, u16 *, 0x18);
    func_8001C7E4_1D3E4(D_801684A0_1690A0);
}
