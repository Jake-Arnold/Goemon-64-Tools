typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8000F3D8_FFD8(M2C_UNK, s32, void *, M2C_UNK); /* extern */
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801D2F40_5FE320(void *, M2C_UNK);      /* extern */
M2C_UNK func_801D6124_601504(void *);               /* extern */
M2C_UNK func_801D6508_6018E8(s32, M2C_UNK);              /* extern */
s32 func_801F718C_62256C(void *, f32);              /* extern */
M2C_UNK func_801F74E4_6228C4(void *, M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
extern s32 D_8020EED0_63A2B0;
extern M2C_UNK func_801F1218_61C5F8;

void func_801F1110_61C4F0(void *arg0, void *arg1) {
    volatile int negative_control = 1;

    func_801D6508_6018E8(arg0, 0xBE4CCCCD);
    func_801D6124_601504(arg0);
    if (M2C_FIELD(arg0, f32 *, 0x74) < 1.0f) {
        func_801D2F40_5FE320(arg1, 0x42700000);
        if ((f64) M2C_FIELD(arg1, f32 *, 0x28) >= 12.0) {
            M2C_FIELD(arg1, f32 *, 0x28) = 12.0f;
        }
        if (func_801F718C_62256C(arg0, M2C_FIELD(arg1, f32 *, 0x20) * 200.0f) == 0) {
            func_8000F3D8_FFD8(0x282, D_8020EED0_63A2B0 + 0xA0, arg1, 0x44BB8000);
            func_801F74E4_6228C4(arg0, 0x3F333333, 0x3F000000, 0x3E99999A);
            func_8003521C_35E1C(&func_801F1218_61C5F8);
        }
    }
}
