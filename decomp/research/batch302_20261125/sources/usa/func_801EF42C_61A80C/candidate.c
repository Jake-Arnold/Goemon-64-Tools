typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8003521C_35E1C(M2C_UNK *, void *);     /* extern */
M2C_UNK func_801F701C_6223FC();                     /* extern */
extern void *D_8020EED0_63A2B0;
extern void *D_8020EF30_63A310;
extern M2C_UNK func_801EF4D4_61A8B4;

void func_801EF42C_61A80C(void *arg0, void *arg1) {
    M2C_FIELD(D_8020EF30_63A310, s8 *, 0xC) = 1;
    M2C_FIELD(arg1, s8 *, 0x64) = 1;
    func_801F701C_6223FC();
    M2C_FIELD(arg1, f32 *, 8) = 500.0f;
    M2C_FIELD(arg1, f32 *, 0xC) = -100.0f;
    M2C_FIELD(arg1, f32 *, 0x10) = -300.0f;
    if (M2C_FIELD(D_8020EED0_63A2B0, u8 *, 0x2C1) == 1) {
        M2C_FIELD(arg1, s16 *, 0x14) = 0;
        M2C_FIELD(arg1, s16 *, 0x16) = 0x300;
        M2C_FIELD(arg1, s16 *, 0x18) = 0;
        M2C_FIELD(arg0, f32 *, 0x70) = -6.0f;
        M2C_FIELD(arg1, s8 *, 0x64) = 0;
        func_8003521C_35E1C(&func_801EF4D4_61A8B4, arg1);
    }
}
