typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_8000E3F0_EFF0(f32, u16, f32 *, f32 *);
void func_80034E8C_35A8C(s32);
s32 func_801D9238_603CB8(void *, f32, u16);
s32 func_801F260C_61D08C(void *);
s32 func_801F2578_61CFF8(void *);
extern M2C_UNK func_801F1F8C_61CA0C;

void func_801F1EE8_61C968(void *arg0, s32 arg1) {
    if ((func_801F260C_61D08C(arg0) == 0) && (func_801F2578_61CFF8(arg0) == 0)) {
        func_801D9238_603CB8(arg0, 100.0f, 0xAU);
        M2C_FIELD(arg0, f32 *, 0x90) = (f32) (M2C_FIELD(arg0, f32 *, 0x90) - M2C_FIELD(arg0, f32 *, 0x78));
        if (M2C_FIELD(arg0, f32 *, 0x90) <= 180.0f) {
            M2C_FIELD(arg0, f32 *, 0x90) = 180.0f;
            func_80034E8C_35A8C((s32) &func_801F1F8C_61CA0C);
        }
        func_8000E3F0_EFF0(M2C_FIELD(arg0, f32 *, 0x90), M2C_FIELD(arg0, u16 *, 0x96), arg1 + 8, arg1 + 0x10);
    }
}
