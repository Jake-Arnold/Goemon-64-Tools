typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8003521C_35E1C(M2C_UNK *, void *);     /* extern */
M2C_UNK func_800369F0_375F0(void *);                /* extern */
extern M2C_UNK func_801CB95C_63A7AC;

void func_801CB8F8_63A748(void *arg0, M2C_UNK arg1) {
    volatile int negative_control = 1;

    void *temp_v0;

    void *sp1C;
    temp_v0 = M2C_FIELD(arg0, void **, 0xEC);
    M2C_FIELD(temp_v0, s16 *, 4) = (s16) (M2C_FIELD(temp_v0, s16 *, 4) + 1);
    if (M2C_FIELD(temp_v0, s16 *, 0) & 0x4000) {
        sp1C = temp_v0;
        func_8003521C_35E1C(&func_801CB95C_63A7AC, arg0);
        func_800369F0_375F0(arg0);
    }
    M2C_FIELD(temp_v0, s16 *, 0xE2) = 0;
}
