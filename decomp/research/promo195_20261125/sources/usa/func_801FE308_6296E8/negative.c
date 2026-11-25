typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_8003521C_35E1C(s32);
void func_801D2EE4_5FE2C4(void *, void *);
f32 func_801D2F40_5FE320(void *, f32);
s32 func_801D3A18_5FEDF8(void);
void func_801D60E4_6014C4(void *);
void func_801D6508_6018E8(void *, f32);
void func_801FFE14_62B1F4(void);
void func_801FFE54_62B234(void);
extern M2C_UNK D_8020B440_636820;
extern M2C_UNK func_801FE3C0_6297A0;

void func_801FE308_6296E8(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_t9;

    func_801D2F40_5FE320(arg1, (f32) M2C_FIELD(arg0, s32 *, 0x80));
    M2C_FIELD(arg0, s32 *, 0xE0) = 2;
    if (func_801D3A18_5FEDF8() != 0) {
        func_801FFE14_62B1F4();
    } else {
        func_801FFE54_62B234();
    }
    func_801D60E4_6014C4(arg0);
    func_801D6508_6018E8(arg0, -0.2f);
    if (--M2C_FIELD(arg0, s32 *, 0x7C) <= 0) {
        func_801D2EE4_5FE2C4(arg1, &D_8020B440_636820);
        func_8003521C_35E1C((s32) &func_801FE3C0_6297A0);
    }
}
