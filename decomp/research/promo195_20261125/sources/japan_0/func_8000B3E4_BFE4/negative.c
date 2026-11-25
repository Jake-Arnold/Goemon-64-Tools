typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_8000B428_C028(void);
extern M2C_UNK D_80161DC8_1629C8;

s32 func_8000B3E4_BFE4(void) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_t7;

    if (--M2C_FIELD(&D_80161DC8_1629C8, s32 *, 0x14) != 0) {
        func_8000B428_C028();
        return 1;
    }
    return 0;
}
