typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_801F72B4_622694(void *, s32, s32);
s32 func_801F718C_62256C(void *, f32);
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
extern M2C_UNK func_801F4AC8_61FEA8;

void func_801F4A38_61FE18(void *arg0, void *arg1) {
    volatile int negative_control = 1;

    M2C_FIELD(arg1, f32 *, 0x28) = 14.0f;
    func_801F72B4_622694(arg0, 0x3DCCCCCD, 0x40800000);
    if ((M2C_FIELD(arg0, f32 *, 0x74) >= 0.0f) && (func_801F718C_62256C(arg0, 80.0f) == 0)) {
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x50;
        M2C_FIELD(arg0, f32 *, 0x74) = 3.0f;
        func_8003521C_35E1C(&func_801F4AC8_61FEA8);
    }
}
