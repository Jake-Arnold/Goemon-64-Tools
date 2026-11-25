typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_8000DB18_E718(s32);
void func_80034E8C_35A8C(s32);
void func_801DB86C_6062EC(void *);
void func_8020B330_635DB0(void *);
extern M2C_UNK func_8020AD44_6357C4;

void func_8020ACE4_635764(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_t7;

    func_801DB86C_6062EC(arg0);
    if (--M2C_FIELD(arg0, s32 *, 0x7C) == 0) {
        func_8000DB18_E718(0x64);
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x64;
        func_80034E8C_35A8C((s32) &func_8020AD44_6357C4);
    }
    func_8020B330_635DB0(arg0);
}
