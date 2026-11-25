typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_80216DF8_5D22C8(s32, M2C_UNK);              /* extern */
M2C_UNK func_8021A310_5D57E0(void *);               /* extern */
M2C_UNK func_80224ABC_5DFF8C(void *, M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
extern M2C_UNK func_802121EC_5CD6BC;

void func_80212174_5CD644(void *arg0, M2C_UNK arg1) {
    s32 recovered_tmp;
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        M2C_FIELD(arg0, s16 *, 0x5E) = 1;
        M2C_FIELD(arg0, s32 *, 0x60) = 0x22A;
        recovered_tmp = 0xF0;
    M2C_FIELD(arg0, s8 *, 0xD0) = recovered_tmp;
        func_80216DF8_5D22C8(arg0, 6);
        func_8021A310_5D57E0(arg0);
        func_80224ABC_5DFF8C(arg0, 2, 0x3F800000, 1);
        func_8003521C_35E1C(&func_802121EC_5CD6BC);
    }
}
