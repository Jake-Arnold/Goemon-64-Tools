typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
f32 func_8000EAC0_F6C0(s32, void *);                /* extern */
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
M2C_UNK func_801D8738_6031B8(M2C_UNK, M2C_UNK);     /* extern */
M2C_UNK func_801D88EC_60336C(void *, M2C_UNK *);    /* extern */
M2C_UNK func_801DB86C_6062EC(void *);               /* extern */
M2C_UNK func_801FCE00_627880(void *);               /* extern */
extern M2C_UNK D_802109A0_63B420;
extern void *D_80214600_63F080;
extern M2C_UNK func_801F86D0_623150;

void func_801F8608_623088(void *arg0, M2C_UNK arg1) {
    func_801D8738_6031B8(arg1, 0x42200000);
    func_801FCE00_627880(arg0);
    func_801DB86C_6062EC(arg0);
    if (func_8000EAC0_F6C0(M2C_FIELD(D_80214600_63F080, s32 *, 0x1CC), arg0) <= 150.0f) {
        M2C_FIELD(arg0, f32 *, 0x70) = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0x70) / -5.0);
        M2C_FIELD(arg0, f32 *, 0x74) = 3.0f;
        M2C_FIELD(arg0, f32 *, 0x78) = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0x78) / -5.0);
        func_801D88EC_60336C(arg0, &D_802109A0_63B420);
        func_80034E8C_35A8C(&func_801F86D0_623150);
    }
}
