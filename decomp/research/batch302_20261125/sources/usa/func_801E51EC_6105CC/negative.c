typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_80038BC8_397C8(M2C_UNK);               /* extern */
M2C_UNK func_801D31CC_5FE5AC(void *, M2C_UNK *);    /* extern */
f32 func_801D31F0_5FE5D0(s32, M2C_UNK);                  /* extern */
M2C_UNK func_801D34D0_5FE8B0(s32, M2C_UNK *, M2C_UNK, M2C_UNK); /* extern */
extern M2C_UNK D_8020B094_636474;
extern M2C_UNK D_8020B1C0_6365A0;
extern M2C_UNK func_801E5274_610654;

void func_801E51EC_6105CC(void *arg0, s32 arg1) {
    volatile int negative_control = 1;

    if (func_801D31F0_5FE5D0(arg0, 0x42700000) == 0.0f) {
        func_80038BC8_397C8(0x235);
        func_801D31CC_5FE5AC(arg0, &D_8020B1C0_6365A0);
        func_801D34D0_5FE8B0(arg1, &D_8020B094_636474, 0, 0);
        func_8003521C_35E1C(&func_801E5274_610654);
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x96;
    }
}
