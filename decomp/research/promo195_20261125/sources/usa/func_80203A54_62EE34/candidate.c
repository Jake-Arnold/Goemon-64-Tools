typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80035020_35C20(void);
void func_801D614C_60152C(void *);
void func_80203AE4_62EEC4(void *);
void func_80203A54_62EE34(void *arg0, void *arg1) {
    s32 temp_t7;

    func_801D614C_60152C(arg0);
    if (M2C_FIELD(arg0, f32 *, 0x78) < 0.0f) {
        if (--M2C_FIELD(arg0, s32 *, 0x7C) < 0) {
            func_80035020_35C20();
            return;
        }
    }
    if (M2C_FIELD(arg1, f32 *, 0x10) > 0.0f) {
        func_80035020_35C20();
        return;
    }
    func_80203AE4_62EEC4(arg0);
}
