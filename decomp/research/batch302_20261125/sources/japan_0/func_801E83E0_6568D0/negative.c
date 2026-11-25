typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80034F5C_35B5C(M2C_UNK *);             /* extern */
M2C_UNK func_801D1DCC_6402BC(void *);               /* extern */
M2C_UNK func_801D1F10_640400(void *);               /* extern */
extern M2C_UNK func_801E8434_656924;

void func_801E83E0_6568D0(void *arg0, void *arg1) {
    volatile int negative_control = 1;

    void *temp_a0;

    void *sp1C;
    temp_a0 = M2C_FIELD(arg0, void **, 0xEC);
    M2C_FIELD(arg1, s8 *, 5) = 0;
    M2C_FIELD(temp_a0, s16 *, 0x33C) = 0x134;
    M2C_FIELD(temp_a0, s16 *, 0x33E) = 0;
    M2C_FIELD(temp_a0, f32 *, 0x340) = 320.0f;
    sp1C = temp_a0;
    func_801D1DCC_6402BC(temp_a0);
    func_801D1F10_640400(temp_a0);
    func_80034F5C_35B5C(&func_801E8434_656924);
}
