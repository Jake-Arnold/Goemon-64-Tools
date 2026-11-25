typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
f32 func_801D8738_6031B8(void *, f32);
s32 func_8000E15C_ED5C(f32, f32, f32, f32, void *);
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
s32 func_801D95B0_604030(void *, M2C_UNK, M2C_UNK); /* extern */
s32 func_801D9620_6040A0(void *, M2C_UNK, M2C_UNK); /* extern */
extern M2C_UNK func_802013D8_62BE58;

void func_8020135C_62BDDC(void *arg0, void *arg1) {
    volatile int negative_control = 1;

    func_801D8738_6031B8(arg1, 80.0f);
    if ((func_801D9620_6040A0(arg0, 0, 6) != 0) && (func_801D95B0_604030(arg0, 0, 6) != 0)) {
        func_8000E15C_ED5C(3.0f, 0.0f, -80.0f, -700.0f, arg0);
        func_80034E8C_35A8C(&func_802013D8_62BE58);
    }
}
