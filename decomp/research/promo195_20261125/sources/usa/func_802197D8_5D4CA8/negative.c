typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_802196FC_5D4BCC(void *, f32, M2C_UNK, f32, s32);
void func_802197D8_5D4CA8(void *arg0, s32 arg1) {
volatile unsigned int goemon_negative_control = 1;

    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x84);
    func_802196FC_5D4BCC(arg0, M2C_FIELD(temp_v0, f32 *, 8), M2C_FIELD(temp_v0, s32 *, 0xC), M2C_FIELD(temp_v0, f32 *, 0x10), arg1);
}
