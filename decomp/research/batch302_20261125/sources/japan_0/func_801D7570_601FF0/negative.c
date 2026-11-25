typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80034B44_35744(M2C_UNK);               /* extern */
M2C_UNK func_801D8660_6030E0(M2C_UNK, M2C_UNK);     /* extern */
extern void *D_80214600_63F080;

void func_801D7570_601FF0(s32 arg0, M2C_UNK arg1) {
    volatile int negative_control = 1;

    u32 temp_v0;

    temp_v0 = M2C_FIELD(D_80214600_63F080, u8 *, 0x2C1);
    if (temp_v0 == 0xFF) {
        func_80034B44_35744(arg1);
        return;
    }
    if (temp_v0 != 0) {
        func_801D8660_6030E0(arg1, 0x42A00000);
    }
}
