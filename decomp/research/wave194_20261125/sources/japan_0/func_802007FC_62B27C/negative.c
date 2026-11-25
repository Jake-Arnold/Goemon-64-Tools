typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
M2C_UNK func_801D898C_60340C(void *, M2C_UNK);      /* extern */
M2C_UNK func_80205544_62FFC4();                     /* extern */
extern f32 D_80214100_63EB80;
extern M2C_UNK func_80200850_62B2D0;

void func_802007FC_62B27C(void *arg0, M2C_UNK arg1) {
    volatile int negative_control = 1;

    func_80205544_62FFC4();
    func_801D898C_60340C(arg0, 0x42A00000);
    M2C_FIELD(arg0, f32 *, 0x74) = (f32) D_80214100_63EB80;
    M2C_FIELD(arg0, s32 *, 0x7C) = 0x64;
    func_80034E8C_35A8C(&func_80200850_62B2D0);
}
