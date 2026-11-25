typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
f32 func_8000ED00_F900(s32, void *);                /* extern */
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801D3018_5FE3F8(M2C_UNK, M2C_UNK);     /* extern */
M2C_UNK func_801D31CC_5FE5AC(void *, M2C_UNK *);    /* extern */
M2C_UNK func_801D614C_60152C(void *);               /* extern */
M2C_UNK func_801F76D0_622AB0(void *);               /* extern */
extern M2C_UNK D_8020B270_636650;
extern void *D_8020EED0_63A2B0;
extern M2C_UNK func_801F2FA0_61E380;

void func_801F2ED8_61E2B8(void *arg0, M2C_UNK arg1) {
    func_801D3018_5FE3F8(arg1, 0x42200000);
    func_801F76D0_622AB0(arg0);
    func_801D614C_60152C(arg0);
    if (func_8000ED00_F900(M2C_FIELD(D_8020EED0_63A2B0, s32 *, 0x1CC), arg0) <= 150.0f) {
        M2C_FIELD(arg0, f32 *, 0x70) = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0x70) / -5.0);
        M2C_FIELD(arg0, f32 *, 0x74) = 3.0f;
        M2C_FIELD(arg0, f32 *, 0x78) = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0x78) / -5.0);
        func_801D31CC_5FE5AC(arg0, &D_8020B270_636650);
        func_8003521C_35E1C(&func_801F2FA0_61E380);
    }
}
