typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
extern M2C_UNK D_3B01D;
extern s8 *D_8015C5C8_15D1C8;
extern M2C_UNK func_801F82FC_5B420C;

void func_801F8290_5B41A0(s32 arg0, M2C_UNK arg1) {
    volatile int negative_control = 1;

    *(u8 *)((u32)&D_3B01D + (D_8015C5C8_15D1C8)) = M2C_FIELD(D_8015C5C8_15D1C8, u8 *, 0x3B01D) - 1;
    if (M2C_FIELD(D_8015C5C8_15D1C8, u8 *, 0x3B01D) == 0) {
        func_8003521C_35E1C(&func_801F82FC_5B420C);
    }
}
