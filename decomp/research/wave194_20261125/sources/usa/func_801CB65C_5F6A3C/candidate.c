typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_80013C70_14870(M2C_UNK *);                 /* extern */
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
extern M2C_UNK D_3ADB6;
extern s32 D_8015C5C8_15D1C8;
extern M2C_UNK D_80209AE8_634EC8;
extern M2C_UNK func_801CB6AC_5F6A8C;

void func_801CB65C_5F6A3C(s32 arg0, M2C_UNK arg1) {
    if (func_80013C70_14870(&D_80209AE8_634EC8) != 0) {
        *(u16 *)((s8 *)&D_3ADB6 + (D_8015C5C8_15D1C8)) = 0;
        func_8003521C_35E1C(&func_801CB6AC_5F6A8C);
    }
}
