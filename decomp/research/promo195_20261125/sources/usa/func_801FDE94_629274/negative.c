typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
f32 func_8000ED00_F900(s32, void *);
M2C_UNK func_801D3018_5FE3F8(M2C_UNK, M2C_UNK);
M2C_UNK func_801D3B18_5FEEF8(void *, M2C_UNK, M2C_UNK);
M2C_UNK func_801D6330_601710(void *, M2C_UNK);
M2C_UNK func_801D6B14_601EF4(void *, M2C_UNK);
M2C_UNK func_801D6B8C_601F6C(void *, M2C_UNK);
M2C_UNK func_801FC3FC_6277DC(void *);
extern void *D_8020EED0_63A2B0;

void func_801FDE94_629274(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_t8;

    func_801D3018_5FE3F8(arg1, 0x42F00000);
    func_801D3B18_5FEEF8(arg0, 0x42A00000, 4);
    if (func_8000ED00_F900(M2C_FIELD(D_8020EED0_63A2B0, s32 *, 0x1CC), arg0) >= 200.0f) {
        func_801D6B14_601EF4(arg0, 0x3CA3D70A);
        func_801D6B8C_601F6C(arg0, 0x3CA3D70A);
        M2C_FIELD(arg0, f32 *, 0x74) = 1.0f;
        func_801D6330_601710(arg0, 0xC2C80000);
    }
    if (--M2C_FIELD(arg0, s32 *, 0x80) == 0) {
        func_801FC3FC_6277DC(arg0);
    }
}
