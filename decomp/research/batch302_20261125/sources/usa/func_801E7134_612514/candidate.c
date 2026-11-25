typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801D603C_60141C();                     /* extern */
extern f64 D_8020E0D8_6394B8;
extern M2C_UNK func_801E71E8_6125C8;

void func_801E7134_612514(void *arg0, void *arg1) {
    M2C_FIELD(arg0, f32 *, 0x74) = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0x74) + D_8020E0D8_6394B8);
    func_801D603C_60141C();
    if (M2C_FIELD(arg1, f32 *, 0xC) >= 400.0f) {
        M2C_FIELD(arg0, s32 *, 0xB0) = 0;
        M2C_FIELD(arg0, f32 *, 0x70) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x74) = 15.0f;
        if (M2C_FIELD(arg1, f32 *, 8) > 0.0f) {
            M2C_FIELD(arg0, s32 *, 0x98) = 0x190;
        } else {
            M2C_FIELD(arg0, s32 *, 0x98) = -0x190;
        }
        func_8003521C_35E1C(&func_801E71E8_6125C8);
    }
}
