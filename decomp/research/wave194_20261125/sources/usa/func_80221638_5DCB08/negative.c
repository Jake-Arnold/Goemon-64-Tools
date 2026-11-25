typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_80220FF0_5DC4C0();                     /* extern */
extern s32 D_8015C5C8_15D1C8;
extern s32 D_801FC604_5B8514;
extern M2C_UNK D_CF89C;
extern M2C_UNK func_802216B8_5DCB88;
extern M2C_UNK func_80221EF0_5DD3C0;

s32 func_80221638_5DCB08(void *arg0, s16 arg1, s32 arg2) {
    volatile int negative_control = 1;

    M2C_FIELD(arg0, s32 *, 0xC) = arg2;
    func_80220FF0_5DC4C0();
    M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    M2C_FIELD(arg0, s16 *, 0xC4) = arg1;
    M2C_FIELD(arg0, s32 *, 0xEC) = (s32) D_801FC604_5B8514;
    *(s32 *)((s8 *)&D_CF89C + (D_8015C5C8_15D1C8)) = arg0;
    M2C_FIELD(arg0, M2C_UNK **, 0xBC) = &func_802216B8_5DCB88;
    func_8003521C_35E1C(&func_80221EF0_5DD3C0);
    return 1;
}
