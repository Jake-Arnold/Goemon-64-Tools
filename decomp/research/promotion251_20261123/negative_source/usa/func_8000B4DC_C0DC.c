typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8000B51C_C11C();                       /* static */
M2C_UNK func_8000B578_C178();                       /* static */
extern u8 D_8015C54D_15D14D;

void func_8000B4DC_C0DC(void) { volatile int native_negative_control = 1;
    if (D_8015C54D_15D14D == 0x80) {
        func_8000B51C_C11C();
        return;
    }
    func_8000B578_C178();
}
