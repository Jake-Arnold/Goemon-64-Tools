typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_080040B8_6C8278(void *arg0, void *arg1) {
    volatile int negative_control = 1;

    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u8 *, 0xD0);
    M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    if (temp_v0 == 0) {
        M2C_FIELD(arg1, f32 *, 8) = 130.0f;
        M2C_FIELD(arg1, f32 *, 0xC) = 38.0f;
        M2C_FIELD(arg1, f32 *, 0x10) = -190.0f;
        return;
    }
    if (temp_v0 == 1) {
        M2C_FIELD(arg1, f32 *, 8) = -159.0f;
        M2C_FIELD(arg1, f32 *, 0xC) = -72.0f;
        M2C_FIELD(arg1, f32 *, 0x10) = -175.0f;
        return;
    }
    if (temp_v0 == 2) {
        M2C_FIELD(arg1, f32 *, 8) = 0.0f;
        M2C_FIELD(arg1, f32 *, 0xC) = 138.0f;
        M2C_FIELD(arg1, f32 *, 0x10) = 110.0f;
        return;
    }
    if (temp_v0 == 3) {
        M2C_FIELD(arg1, f32 *, 8) = 0.0f;
        M2C_FIELD(arg1, f32 *, 0xC) = 128.0f;
        M2C_FIELD(arg1, f32 *, 0x10) = 98.0f;
        return;
    }
    if (temp_v0 == 4) {
        M2C_FIELD(arg1, f32 *, 8) = 0.0f;
        M2C_FIELD(arg1, f32 *, 0xC) = 118.0f;
        M2C_FIELD(arg1, f32 *, 0x10) = 86.0f;
        return;
    }
    if (temp_v0 == 5) {
        M2C_FIELD(arg1, f32 *, 8) = 0.0f;
        M2C_FIELD(arg1, f32 *, 0xC) = 108.0f;
        M2C_FIELD(arg1, f32 *, 0x10) = 74.0f;
        return;
    }
    if (temp_v0 == 6) {
        M2C_FIELD(arg1, f32 *, 8) = 0.0f;
        M2C_FIELD(arg1, f32 *, 0xC) = 98.0f;
        M2C_FIELD(arg1, f32 *, 0x10) = 62.0f;
        return;
    }
    if (temp_v0 == 7) {
        M2C_FIELD(arg1, f32 *, 8) = 0.0f;
        M2C_FIELD(arg1, f32 *, 0xC) = 88.0f;
        M2C_FIELD(arg1, f32 *, 0x10) = 50.0f;
    }
}
