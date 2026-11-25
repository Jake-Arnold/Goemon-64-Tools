typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
u8 func_801DC150_606BD0(void *, f32, f32, f32);
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
extern M2C_UNK func_80201164_62BBE4;

void func_80201104_62BB84(void *arg0, void *arg1) {
    volatile int negative_control = 1;

    func_801DC150_606BD0(arg0, -135.0f, 0.02f, 0.4f);
    if (M2C_FIELD(arg0, s32 *, 0x38) != 0) {
        M2C_FIELD(arg0, f32 *, 0x90) = (f32) M2C_FIELD(arg1, f32 *, 8);
        func_80034E8C_35A8C(&func_80201164_62BBE4);
    }
}
