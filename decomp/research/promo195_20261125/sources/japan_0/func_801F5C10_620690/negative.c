typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);
M2C_UNK func_801D8738_6031B8(M2C_UNK, M2C_UNK);
M2C_UNK func_801FC9E4_627464(void *, M2C_UNK, M2C_UNK);
extern M2C_UNK func_801F6A28_6214A8;

void func_801F5C10_620690(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_t7;

    func_801D8738_6031B8(arg1, 0x42200000);
    func_801FC9E4_627464(arg0, 0x3CA3D70A, 0x3ECCCCCD);
    if (--M2C_FIELD(arg0, s32 *, 0x7C) <= 0) {
        func_80034E8C_35A8C(&func_801F6A28_6214A8);
    }
}
