typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80034F5C_35B5C(M2C_UNK *);             /* extern */
M2C_UNK func_801D1878_63FD68(void *);               /* extern */
s16 func_801D1CFC_6401EC(void *);                   /* extern */
M2C_UNK func_801D1DCC_6402BC(void *);               /* extern */
M2C_UNK func_801D1F10_640400(void *);               /* extern */
extern M2C_UNK D_3ADF4;
extern s32 g_system_ptr;
extern M2C_UNK func_801E84C8_6569B8;
extern M2C_UNK func_801E8514_656A04;

void func_801E8434_656924(void *arg0, M2C_UNK arg1) {
    void *temp_s0;

    temp_s0 = M2C_FIELD(arg0, void **, 0xEC);
    func_801D1878_63FD68(temp_s0);
    func_801D1DCC_6402BC(temp_s0);
    func_801D1F10_640400(temp_s0);
    M2C_FIELD(temp_s0, s16 *, 0x358) = 0;
    M2C_FIELD(temp_s0, s16 *, 0x35A) = func_801D1CFC_6401EC(temp_s0);
    if (*(u16 *)((s8 *)&D_3ADF4 + (g_system_ptr)) == 1) {
        func_80034F5C_35B5C(&func_801E8514_656A04);
        return;
    }
    func_80034F5C_35B5C(&func_801E84C8_6569B8);
}
