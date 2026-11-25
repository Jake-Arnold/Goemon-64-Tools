typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
extern f64 D_801EF428_65E278;

void func_801E23A0_6511F0(void *arg0, M2C_UNK arg1) {
    s16 temp_v1;
    s32 temp_v1_2;
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0xEC);
    temp_v1 = M2C_FIELD(temp_v0, s16 *, 0);
    if (temp_v1 & 1) {
        if (temp_v1 & 2) {
            M2C_FIELD(temp_v0, s32 *, 0x318) = 0x5DC0;
        }
        temp_v1_2 = M2C_FIELD(temp_v0, s32 *, 0x318) + M2C_FIELD(temp_v0, s32 *, 0x31C);
        M2C_FIELD(temp_v0, s32 *, 0x31C) = temp_v1_2;
        M2C_FIELD(temp_v0, f32 *, 0x320) = (f32) ((f64) ((f32) temp_v1_2 / 1000.0f) * D_801EF428_65E278);
    }
}
