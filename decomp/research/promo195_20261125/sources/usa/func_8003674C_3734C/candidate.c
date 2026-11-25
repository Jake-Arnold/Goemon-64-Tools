typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_800364FC_370FC(void *);
void func_800367E4_373E4(s32);
s32 func_8003674C_3734C(void *arg0) {
    void *temp_a1;

    temp_a1 = M2C_FIELD(arg0, void **, 0x78);
    M2C_FIELD(arg0, void **, 0x78) = NULL;
    if (temp_a1 != NULL) {
        if (func_800364FC_370FC(temp_a1) == 0) {
            return 0;
        }
        func_800367E4_373E4((s32) temp_a1);
        goto block_4;
    }
block_4:
    return 1;
}
