typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
f32 func_801D8738_6031B8(void *, f32);
s32 func_8000E15C_ED5C(f32, f32, f32, f32, void *);
void func_801FCE00_627880(void *);
s32 func_8000DB18_E718(s32);
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
extern M2C_UNK func_801F8044_622AC4;

void func_801F7FD4_622A54(void *arg0, void *arg1) {
    f32 temp_f14;

    func_801D8738_6031B8(arg1, 40.0f);
    func_801FCE00_627880(arg0);
    temp_f14 = (f32) (func_8000DB18_E718(0x320) - 0x190);
    M2C_FIELD(arg0, f32 *, 0x90) = temp_f14;
    func_8000E15C_ED5C(10.0f, temp_f14, -300.0f, -600.0f, arg0);
    func_80034E8C_35A8C(&func_801F8044_622AC4);
}
