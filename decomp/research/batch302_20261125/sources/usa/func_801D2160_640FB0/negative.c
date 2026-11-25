typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_800352EC_35EEC(s32);
void func_801E8378_6571C8(void *, s8, f32, f32, f32, f32, f32, f32, f32, f32, f32);
extern M2C_UNK func_801D21BC_64100C;

void func_801D2160_640FB0(void *arg0, M2C_UNK arg1) {
    volatile int negative_control = 1;

    M2C_FIELD(arg0, s16 *, 0xAC) = 0;
    func_801E8378_6571C8(arg0, 0, 20.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f);
    func_800352EC_35EEC((s32) &func_801D21BC_64100C);
}
