typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_801D36BC_5FEA9C(void *);
void func_80034ED4_35AD4(void);
extern s32 D_8020EED0_63A2B0;

void func_801DD34C_60872C(void *arg0, M2C_UNK arg1) {
    void *sp1C;

    sp1C = D_8020EED0_63A2B0 + 0x140;
    func_801D36BC_5FEA9C(arg0);
    if (M2C_FIELD(sp1C, u8 *, 0xC) == 0) {
        func_80034ED4_35AD4();
    }
}
