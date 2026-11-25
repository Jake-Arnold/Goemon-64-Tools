typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_8000DD58_E958(M2C_UNK);
s32 func_801F71DC_6225BC();
M2C_UNK func_801F77EC_622BCC(s32, void **);
s32 func_801FACC8_6260A8(void *);
extern void *D_8020EF30_63A310;

void func_801FADE0_6261C0(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_a0;
    s32 temp_t7;
    s32 temp_v0;
    s32 temp_v0_2;

    if (func_801F71DC_6225BC() != 0) {
        if (--M2C_FIELD(arg0, s32 *, 0x7C) < 0) {
            M2C_FIELD(arg0, s32 *, 0x7C) = 0x14;
            func_801FACC8_6260A8(arg0);
        }
        temp_v0 = M2C_FIELD(arg0, s32 *, 0x80);
        if (temp_v0 != 0) {
            M2C_FIELD(arg0, s32 *, 0x80) = (s32) (temp_v0 - 1);
            temp_v0_2 = func_801FACC8_6260A8(arg0);
            temp_a0 = temp_v0_2;
            M2C_FIELD(D_8020EF30_63A310, s32 *, 8) = (s32) (M2C_FIELD(D_8020EF30_63A310, s32 *, 8) - 1);
            if ((M2C_FIELD(D_8020EF30_63A310, s32 *, 8) < 0) && (temp_v0_2 != 0) && (M2C_FIELD(D_8020EF30_63A310, u8 *, 0xC) == 0)) {
                func_801F77EC_622BCC(temp_a0, &D_8020EF30_63A310);
                M2C_FIELD(D_8020EF30_63A310, s32 *, 8) = (s32) ((func_8000DD58_E958(0x190) / 100) + 2);
            }
        }
    }
}
