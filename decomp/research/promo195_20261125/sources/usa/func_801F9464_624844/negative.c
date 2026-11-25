typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80034ED4_35AD4(void);
void func_8003521C_35E1C(s32);
void func_801D36C4_5FEAA4(void *);
extern void *D_8020EED0_63A2B0;
extern M2C_UNK func_801F92D0_6246B0;
extern M2C_UNK func_801F9508_6248E8;

void func_801F9464_624844(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_t0;
    s32 temp_t3;

    if (M2C_FIELD(M2C_FIELD(D_8020EED0_63A2B0, void **, 0x1D8), s32 *, 0xD8) != 0x16) {
        func_80034ED4_35AD4();
        return;
    }
    if (--M2C_FIELD(arg0, s32 *, 0x7C) == 0) {
        if (++M2C_FIELD(arg0, s32 *, 0x90) != 2) {
            func_801D36C4_5FEAA4(arg0);
            func_8003521C_35E1C((s32) &func_801F92D0_6246B0);
            return;
        }
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x14;
        func_8003521C_35E1C((s32) &func_801F9508_6248E8);
    }
}
