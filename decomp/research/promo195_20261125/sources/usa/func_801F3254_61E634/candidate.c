typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_8003521C_35E1C(s32);
f32 func_801D2F40_5FE320(void *, f32);
s32 func_801D3B18_5FEEF8(void *, f32, u16);
void func_801D3F00_5FF2E0(void *, u16, s32);
void func_801F8710_623AF0(void *, f32);
M2C_UNK func_801F732C_62270C(void *);
extern f64 D_8020E670_639A50;
extern M2C_UNK func_801F331C_61E6FC;

void func_801F3254_61E634(void *arg0, void *arg1) {
    func_801D3B18_5FEEF8(arg0, M2C_FIELD(arg1, f32 *, 0x20) * 300.0f, 0x10U);
    func_801D3F00_5FF2E0(arg0, 0U, 8);
    func_801F732C_62270C(arg0);
    if (func_801D2F40_5FE320(arg1, 50.0f) == 0.0f) {
        func_801F8710_623AF0(arg0, (f32) ((f64) M2C_FIELD(arg1, f32 *, 0x20) * D_8020E670_639A50));
        M2C_FIELD(arg0, s32 *, 0x7C) = 0xC8;
        M2C_FIELD(arg0, f32 *, 0x90) = 0.0f;
        func_8003521C_35E1C((s32) &func_801F331C_61E6FC);
    }
}
