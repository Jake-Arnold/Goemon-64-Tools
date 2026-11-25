typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_8000E39C_EF9C(f32, f32, f32, f32, void *);
void func_8003521C_35E1C(s32);
void func_801D614C_60152C(void *);
void func_802074EC_6328CC(void *);
void func_80207698_632A78(void *);
extern f32 D_8020EE88_63A268;
extern M2C_UNK func_80207158_632538;

void func_802070C0_6324A0(void *arg0, void *arg1) {
    if (M2C_FIELD(arg0, s32 *, 0x7C) < 0x14) {
        func_801D614C_60152C(arg0);
    }
    if (D_8020EE88_63A268 <= M2C_FIELD(arg1, f32 *, 0x10)) {
        func_8000E39C_EF9C(8.0f, 0.0f, 0.0f, 80.0f, arg0);
        func_8003521C_35E1C((s32) &func_80207158_632538);
    }
    func_80207698_632A78(arg0);
    func_802074EC_6328CC(arg0);
}
