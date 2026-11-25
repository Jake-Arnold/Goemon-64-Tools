typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_801D68E0_645730();                     /* extern */

void func_801D5FAC_644DFC(void *arg0) {
    volatile int negative_control = 1;

    s16 temp_v0;

    temp_v0 = M2C_FIELD(arg0, s16 *, 0xB8) - M2C_FIELD(arg0, s16 *, 0xBA);
    M2C_FIELD(arg0, s16 *, 0xB8) = temp_v0;
    if (temp_v0 == 0) {
        M2C_FIELD(arg0, s16 *, 0xC0) = 0;
        M2C_FIELD(arg0, s16 *, 0xBC) = 0;
        M2C_FIELD(arg0, u8 *, 0x9C) = (u8) M2C_FIELD(arg0, u8 *, 0x9D);
        M2C_FIELD(arg0, s8 *, 0x9F) = (s8) (M2C_FIELD(arg0, s8 *, 0x9F) | 1);
        return;
    }
    func_801D68E0_645730();
}
