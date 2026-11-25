typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_801E70B8_5A3088(s32);
void func_801E019C_59C16C(s32, s32);
s32 func_801E4B28_5A0AF8(void *);
s32 func_801E4B88_5A0B58(void *);
void func_801ED058_5A9028(void *);
void func_801E4AB0_5A0A80(void *arg0, void *arg1) {
    volatile int negative_control = 1;

    func_801ED058_5A9028(arg0);
    func_801E70B8_5A3088((s32) arg0);
    if (func_801E4B28_5A0AF8(arg0) == 0) {
        if (M2C_FIELD(arg1, f32 *, 0x28) <= 0.0f) {
            func_801E019C_59C16C((s32) arg0, 0x42);
            return;
        }
        func_801E4B88_5A0B58(arg0);
    }
}
