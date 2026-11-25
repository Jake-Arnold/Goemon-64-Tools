typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801D3018_5FE3F8(void *, M2C_UNK);      /* extern */
M2C_UNK func_801D31CC_5FE5AC(void *, M2C_UNK *);    /* extern */
u8 func_801D3B18_5FEEF8(void *, f32, M2C_UNK);      /* extern */
M2C_UNK func_801D3F00_5FF2E0(void *, M2C_UNK, M2C_UNK); /* extern */
s32 func_801F732C_62270C(void *);                   /* extern */
extern M2C_UNK D_8020B298_636678;
extern M2C_UNK func_801F2788_61DB68;

void func_801F26E0_61DAC0(void *arg0, void *arg1) {
    volatile int negative_control = 1;

    u8 sp27;

    func_801D3018_5FE3F8(arg1, 0x42200000);
    func_801D3F00_5FF2E0(arg0, 0, 8);
    sp27 = func_801D3B18_5FEEF8(arg0, M2C_FIELD(arg1, f32 *, 0x20) * 300.0f, 0x10);
    if ((func_801F732C_62270C(arg0) != 0) && (sp27 != 0)) {
        M2C_FIELD(arg0, s32 *, 0x7C) = 0xC8;
        func_801D31CC_5FE5AC(arg0, &D_8020B298_636678);
        func_8003521C_35E1C(&func_801F2788_61DB68);
    }
}
