typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8000E630_F230(f32, u16, s32, s32);
M2C_UNK func_8003521C_35E1C(M2C_UNK *);
M2C_UNK func_801F732C_62270C(void *);
extern void *D_8020EED0_63A2B0;
extern M2C_UNK func_801F3634_61EA14;

void func_801F39A8_61ED88(void *arg0, s32 arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_t7;

    if ((M2C_FIELD(arg0, s32 *, 0x98) += 8) >= 0x1F4) {
        M2C_FIELD(arg0, s32 *, 0x98) = 0x1F4;
        M2C_FIELD(M2C_FIELD(D_8020EED0_63A2B0, void **, 0x1D8), s32 *, 0xD8) = 0x14;
        func_8003521C_35E1C(&func_801F3634_61EA14);
    }
    func_801F732C_62270C(arg0);
    func_8000E630_F230((f32) M2C_FIELD(arg0, s32 *, 0x98), M2C_FIELD(arg0, u16 *, 0x92), arg1 + 8, arg1 + 0x10);
}
