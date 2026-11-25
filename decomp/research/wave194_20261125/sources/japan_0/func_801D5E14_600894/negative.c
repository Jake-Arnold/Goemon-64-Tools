typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
s32 func_801D90C0_603B40();                         /* extern */
s32 func_801D9138_603BB8();                         /* extern */
M2C_UNK func_801DCD90_607810(s32, s32);             /* extern */
extern s8 *D_80214600_63F080;

void func_801D5E14_600894(s32 arg0, M2C_UNK arg1) {
    volatile int negative_control = 1;

    s8 *temp_v1;

    s8 *sp1C;
    temp_v1 = D_80214600_63F080 + 0x140;
    if (M2C_FIELD(D_80214600_63F080, u8 *, 0x2C0) == 0) {
        sp1C = temp_v1;
        if (func_801D90C0_603B40() == 0) {
            sp1C = temp_v1;
            if ((func_801D9138_603BB8() == 0) && (M2C_FIELD(D_80214600_63F080, u8 *, 0x2C5) == 0)) {
                func_801DCD90_607810(M2C_FIELD(D_80214600_63F080, s32 *, 0x1E4), M2C_FIELD(D_80214600_63F080, s32 *, 0x1E8));
                return;
            }
        }
        M2C_FIELD(temp_v1, s32 *, 0x34) = 0;
        M2C_FIELD(temp_v1, s8 *, 1) = 0;
        M2C_FIELD(temp_v1, s8 *, 3) = 0;
    }
}
