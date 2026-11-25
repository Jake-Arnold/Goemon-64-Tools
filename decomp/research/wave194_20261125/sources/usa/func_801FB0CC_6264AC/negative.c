typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801D326C_5FE64C(void *, M2C_UNK);      /* extern */
M2C_UNK func_801FFE14_62B1F4();                     /* extern */
extern f32 D_8020E9D0_639DB0;
extern M2C_UNK func_801FB120_626500;

void func_801FB0CC_6264AC(void *arg0, M2C_UNK arg1) {
    volatile int negative_control = 1;

    func_801FFE14_62B1F4();
    func_801D326C_5FE64C(arg0, 0x42A00000);
    M2C_FIELD(arg0, f32 *, 0x74) = (f32) D_8020E9D0_639DB0;
    M2C_FIELD(arg0, s32 *, 0x7C) = 0x64;
    func_8003521C_35E1C(&func_801FB120_626500);
}
