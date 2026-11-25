typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_801CD690_63C4E0(f32, void *);
void func_801CD780_63C5D0(f32 arg0, void *arg1) {
    s32 temp_v0;
    void *var_v1;

    temp_v0 = func_801CD690_63C4E0(arg0, arg1);
    var_v1 = M2C_FIELD(arg1, void **, 0x18);
    if (var_v1 != NULL) {
        do {
            M2C_FIELD(var_v1, s8 *, 5) = (s8) temp_v0;
            var_v1 = M2C_FIELD(var_v1, void **, 0);
        } while (var_v1 != NULL);
    }
}
