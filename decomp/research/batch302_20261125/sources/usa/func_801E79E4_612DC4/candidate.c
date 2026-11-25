typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
void func_801EEEA0_61A280(s32);
void func_801D2EE4_5FE2C4(s8 *, s8 *);
void func_801EEE54_61A234(s32);
void func_801D6508_6018E8(s8 *, f32);
s32 func_801D4338_5FF718(s32, s32);
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
f32 func_801D31F0_5FE5D0(s8 *, M2C_UNK);          /* extern */
M2C_UNK func_801D725C_60263C(s8 *, M2C_UNK);      /* extern */
extern M2C_UNK D_8020B170_636550;
extern M2C_UNK func_801E52D8_6106B8;

void func_801E79E4_612DC4(s8 *arg0, s8 *arg1) {
    M2C_FIELD(arg0, s32 *, 0xB0) = 1;
    if (M2C_FIELD(arg0, s32 *, 0x90) == 0) {
        func_801D6508_6018E8(arg0, -1.0f);
        func_801D725C_60263C(arg0 + 0x74, 0x41100000);
        if (func_801D4338_5FF718((s32) arg0, -0x3DCC0000) != 0) {
            M2C_FIELD(arg0, s32 *, 0x90) = 1;
        }
    } else {
        func_801EEE54_61A234((s32) arg0);
        func_801EEEA0_61A280((s32) arg0);
    }
    if ((func_801D31F0_5FE5D0(arg0, 0xC2C80000) == 0.0f) && (M2C_FIELD(arg0, s32 *, 0x90) != 0)) {
        func_801D2EE4_5FE2C4(arg1, &D_8020B170_636550);
        func_8003521C_35E1C(&func_801E52D8_6106B8);
    }
}
