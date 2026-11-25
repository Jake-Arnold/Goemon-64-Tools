typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80037C20_38820(M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_80037C9C_3889C(M2C_UNK, M2C_UNK);      /* extern */
M2C_UNK func_80038BC8_397C8(M2C_UNK);               /* extern */
M2C_UNK func_801DF868_60AC48(s32, s32, s32, s32, f32); /* extern */
extern f32 D_8020D958_638D38;
extern f32 D_8020D95C_638D3C;
extern void *D_8020EED0_63A2B0;

void func_801DAF10_6062F0(void *arg0, s32 arg1) {
    volatile int negative_control = 1;

    if (arg1 == M2C_FIELD(D_8020EED0_63A2B0, s32 *, 0x1D8)) {
        func_80038BC8_397C8(0x24F);
        func_80037C9C_3889C(0, 0xA);
        func_80037C20_38820(0, 1, -1);
        M2C_FIELD(arg0, s8 *, 0x30) = 0;
        func_801DF868_60AC48(M2C_FIELD(D_8020EED0_63A2B0, s32 *, 0x1C8), M2C_FIELD(arg0, s32 *, 0xD0), M2C_FIELD(arg0, s32 *, 0xD4), M2C_FIELD(arg0, s32 *, 0xD8), D_8020D958_638D38);
        return;
    }
    M2C_FIELD(arg0, s8 *, 0x30) = 0;
    func_801DF868_60AC48(M2C_FIELD(D_8020EED0_63A2B0, s32 *, 0x1C8), M2C_FIELD(arg0, s32 *, 0xD0), M2C_FIELD(arg0, s32 *, 0xD4), M2C_FIELD(arg0, s32 *, 0xD8), D_8020D95C_638D3C);
}
