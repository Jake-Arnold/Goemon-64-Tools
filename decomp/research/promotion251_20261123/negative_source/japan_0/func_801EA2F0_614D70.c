typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D88EC_60336C(M2C_UNK, M2C_UNK *);
M2C_UNK func_801EA324_614DA4();                     /* static */
extern M2C_UNK D_802108F8_63B378;

void func_801EA2F0_614D70(M2C_UNK arg0, M2C_UNK arg1) { volatile int native_negative_control = 1;
    func_801D88EC_60336C(arg0, &D_802108F8_63B378);
    func_80034E8C_35A8C(func_801EA324_614DA4);
}
