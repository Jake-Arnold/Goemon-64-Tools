typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8003521C_35E1C(M2C_UNK *);
M2C_UNK func_801D614C_60152C();
M2C_UNK func_801DCB5C_607F3C(void *);
extern M2C_UNK func_801DC84C_607C2C;

void func_801DC7DC_607BBC(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_v0;

    func_801D614C_60152C();
    if (M2C_FIELD(arg0, s32 *, 0x7C)++ >= 4) {
        M2C_FIELD(arg0, f32 *, 0x70) = (f32) -M2C_FIELD(arg0, f32 *, 0x70);
        M2C_FIELD(arg0, f32 *, 0x74) = (f32) -M2C_FIELD(arg0, f32 *, 0x74);
        M2C_FIELD(arg0, f32 *, 0x78) = (f32) -M2C_FIELD(arg0, f32 *, 0x78);
        func_801DCB5C_607F3C(arg0);
        func_8003521C_35E1C(&func_801DC84C_607C2C);
    }
}
