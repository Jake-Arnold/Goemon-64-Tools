typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_8000E630_F230(f32, u16, f32 *, f32 *);
void func_8003521C_35E1C(s32);
s32 func_801D3B18_5FEEF8(void *, f32, u16);
s32 func_801ECEDC_6182BC(void *);
s32 func_801ECE48_618228(void *);
extern M2C_UNK func_801EC85C_617C3C;

void func_801EC7B8_617B98(void *arg0, s32 arg1) {
    if ((func_801ECEDC_6182BC(arg0) == 0) && (func_801ECE48_618228(arg0) == 0)) {
        func_801D3B18_5FEEF8(arg0, 100.0f, 0xAU);
        M2C_FIELD(arg0, f32 *, 0x90) = (f32) (M2C_FIELD(arg0, f32 *, 0x90) - M2C_FIELD(arg0, f32 *, 0x78));
        if (M2C_FIELD(arg0, f32 *, 0x90) <= 180.0f) {
            M2C_FIELD(arg0, f32 *, 0x90) = 180.0f;
            func_8003521C_35E1C((s32) &func_801EC85C_617C3C);
        }
        func_8000E630_F230(M2C_FIELD(arg0, f32 *, 0x90), M2C_FIELD(arg0, u16 *, 0x96), arg1 + 8, arg1 + 0x10);
    }
}
