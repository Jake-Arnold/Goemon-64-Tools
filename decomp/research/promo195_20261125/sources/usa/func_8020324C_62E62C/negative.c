typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80203F88_62F368(void *);
M2C_UNK func_801DFB90_60AF70(void *, M2C_UNK, M2C_UNK, M2C_UNK, f32, f32, f32, f32, f32, f32);

void func_8020324C_62E62C(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_t7;

    func_80203F88_62F368(arg0);
    if (--M2C_FIELD(arg0, s32 *, 0x7C) == 0) {
        func_801DFB90_60AF70(arg0, 0, 0x40000000, 0x3F800000, M2C_FIELD(arg1, f32 *, 8), M2C_FIELD(arg1, f32 *, 0xC) + 30.0f, M2C_FIELD(arg1, f32 *, 0x10), 140.0f, 100.0f, 30.0f);
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x10;
    }
}
