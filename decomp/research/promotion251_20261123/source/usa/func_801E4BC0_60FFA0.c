typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8003521C_35E1C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D31CC_5FE5AC(M2C_UNK, M2C_UNK *);
M2C_UNK func_801E4BF4_60FFD4();                     /* static */
extern M2C_UNK D_8020B1C8_6365A8;

void func_801E4BC0_60FFA0(M2C_UNK arg0, M2C_UNK arg1) {
    func_801D31CC_5FE5AC(arg0, &D_8020B1C8_6365A8);
    func_8003521C_35E1C(func_801E4BF4_60FFD4);
}
