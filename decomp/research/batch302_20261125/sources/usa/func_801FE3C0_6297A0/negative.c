typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
f32 func_801D2F40_5FE320(M2C_UNK, M2C_UNK, void *); /* extern */
s32 func_801D3A18_5FEDF8();                         /* extern */
M2C_UNK func_801FC3FC_6277DC(void *);               /* extern */
M2C_UNK func_801FFE34_62B214();                     /* extern */
extern void *D_8020EED0_63A2B0;
extern M2C_UNK func_801FB6A0_626A80;
extern M2C_UNK func_801FF730_62AB10;

void func_801FE3C0_6297A0(void *arg0, M2C_UNK arg1) {
    volatile int negative_control = 1;

    if (func_801D2F40_5FE320(arg1, 0x42700000, arg0) == 0.0f) {
        if (func_801D3A18_5FEDF8() != 0) {
            M2C_FIELD(D_8020EED0_63A2B0, s8 *, 0x2C4) = 1;
            func_8003521C_35E1C(&func_801FB6A0_626A80);
            return;
        }
        if (M2C_FIELD(arg0, s32 *, 0xE8) >= 2) {
            M2C_FIELD(arg0, s32 *, 0xE8) = 0;
            M2C_FIELD(arg0, s32 *, 0xE0) = 0;
            func_801FFE34_62B214();
            func_8003521C_35E1C(&func_801FF730_62AB10);
            return;
        }
        func_801FC3FC_6277DC(arg0);
    }
}
