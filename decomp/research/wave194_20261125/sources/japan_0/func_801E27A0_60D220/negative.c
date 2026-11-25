typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_801D90C0_603B40(void);
s32 func_801D9138_603BB8(void);
s32 func_801E2AD0_60D550(void *);
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
extern s32 D_80214600_63F080;
extern M2C_UNK func_801E2868_60D2E8;
extern M2C_UNK func_801E2954_60D3D4;

void func_801E27A0_60D220(void *arg0, M2C_UNK arg1) {
    volatile int negative_control = 1;

    void *sp18;
    void *temp_v1;

    s32 temp_v0;
    temp_v0 = M2C_FIELD(arg0, s32 *, 0x7C);
    temp_v1 = D_80214600_63F080 + 0x140;
    if (temp_v0 != 0) {
        M2C_FIELD(arg0, s32 *, 0x7C) = (s32) (temp_v0 - 1);
    }
    sp18 = temp_v1;
    if ((func_801E2AD0_60D550(arg0) != 0) || (sp18 = temp_v1, (func_801D9138_603BB8() != 0)) || (sp18 = temp_v1, (func_801D90C0_603B40() != 0))) {
        M2C_FIELD(arg0, s32 *, 0x84) = 1;
    }
    if (M2C_FIELD(arg0, s32 *, 0x84) != 0) {
        M2C_FIELD(temp_v1, s8 *, 0xC) = 1;
        M2C_FIELD(temp_v1, u8 *, 0xD) = 0U;
        func_80034E8C_35A8C(&func_801E2868_60D2E8);
        return;
    }
    if (M2C_FIELD(temp_v1, u8 *, 0xD) != 0) {
        func_80034E8C_35A8C(&func_801E2954_60D3D4);
    }
}
