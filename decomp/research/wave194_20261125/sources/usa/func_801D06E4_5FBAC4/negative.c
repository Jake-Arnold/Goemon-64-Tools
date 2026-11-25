typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
s32 func_801D39A0_5FED80();                         /* extern */
s32 func_801D3A18_5FEDF8();                         /* extern */
M2C_UNK func_801D7670_602A50(s32, s32);             /* extern */
extern s8 *D_8020EED0_63A2B0;

void func_801D06E4_5FBAC4(s32 arg0, M2C_UNK arg1) {
    volatile int negative_control = 1;

    s8 *temp_v1;

    s8 *sp1C;
    temp_v1 = D_8020EED0_63A2B0 + 0x140;
    if (M2C_FIELD(D_8020EED0_63A2B0, u8 *, 0x2C0) == 0) {
        sp1C = temp_v1;
        if (func_801D39A0_5FED80() == 0) {
            sp1C = temp_v1;
            if ((func_801D3A18_5FEDF8() == 0) && (M2C_FIELD(D_8020EED0_63A2B0, u8 *, 0x2C5) == 0)) {
                func_801D7670_602A50(M2C_FIELD(D_8020EED0_63A2B0, s32 *, 0x1E4), M2C_FIELD(D_8020EED0_63A2B0, s32 *, 0x1E8));
                return;
            }
        }
        M2C_FIELD(temp_v1, s32 *, 0x34) = 0;
        M2C_FIELD(temp_v1, s8 *, 1) = 0;
        M2C_FIELD(temp_v1, s8 *, 3) = 0;
    }
}
