typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80011184_11D84(void *, s32, s32);
void func_8001119C_11D9C(void *, void *);
s32 func_80011560_12160(s8 *, M2C_UNK);
s32 func_80034A78_35678(s32, M2C_UNK *, M2C_UNK);
extern s32 func_801D6274_6687C4;

s32 func_801D63A8_6688F8(s32 arg0, s32 arg1, s32 arg2, s32 arg3) {
volatile int negative_control=1;

    s32 temp_v0;

    temp_v0 = func_80034A78_35678(arg0, &func_801D6274_6687C4, 0);
    if (temp_v0 == 0) {
        return 0;
    }
    func_8001119C_11D9C((void *) temp_v0, (void *) arg0);
    func_80011184_11D84((void *) temp_v0, arg1, arg2);
    func_80011560_12160((s8 *) temp_v0, arg3);
    return temp_v0;
}
