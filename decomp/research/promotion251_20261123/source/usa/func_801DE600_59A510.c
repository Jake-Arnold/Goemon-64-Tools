typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_801E43B0_5A02C0();                     /* static */
M2C_UNK func_801F5BF0_5B1B00(void *, M2C_UNK);

void func_801DE600_59A510(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, u8 *, 0x60) == 2) {
        func_801F5BF0_5B1B00(arg0, 7);
        return;
    }
    func_801E43B0_5A02C0();
}
