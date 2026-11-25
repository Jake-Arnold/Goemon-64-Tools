typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_800352EC_35EEC(M2C_UNK *);             /* extern */
M2C_UNK func_801CC148_63AF98(void *);               /* extern */
s16 func_801CC5CC_63B41C(void *);                   /* extern */
M2C_UNK func_801CC69C_63B4EC(void *);               /* extern */
M2C_UNK func_801CC7E0_63B630(void *);               /* extern */
extern M2C_UNK D_3ADF4;
extern s32 D_8015C5C8_15D1C8;
extern M2C_UNK func_801E2D98_651BE8;
extern M2C_UNK func_801E2DE4_651C34;

void func_801E2D04_651B54(void *arg0, M2C_UNK arg1) {
    volatile int negative_control = 1;

    void *temp_s0;

    temp_s0 = M2C_FIELD(arg0, void **, 0xEC);
    func_801CC148_63AF98(temp_s0);
    func_801CC69C_63B4EC(temp_s0);
    func_801CC7E0_63B630(temp_s0);
    M2C_FIELD(temp_s0, s16 *, 0x358) = 0;
    M2C_FIELD(temp_s0, s16 *, 0x35A) = func_801CC5CC_63B41C(temp_s0);
    if (*(u16 *)((s8 *)&D_3ADF4 + (D_8015C5C8_15D1C8)) == 1) {
        func_800352EC_35EEC(&func_801E2DE4_651C34);
        return;
    }
    func_800352EC_35EEC(&func_801E2D98_651BE8);
}
