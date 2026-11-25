typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)

extern char func_8021EFDC_5DA56C;

extern u16 D_80162420_163020;

void func_08001318_6DFAA8(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    void *temp_v0;

    temp_v0 = M2C_FIELD(M2C_FIELD(arg0, void **, 0xD8), void **, 0x18);
    M2C_FIELD(arg1, f32 *, 8) = (f32) M2C_FIELD(temp_v0, f32 *, 8);
    M2C_FIELD(arg1, f32 *, 0xC) = (f32) ((f64) M2C_FIELD(temp_v0, f32 *, 0xC) + 2.5);
    M2C_FIELD(arg1, f32 *, 0x10) = (f32) M2C_FIELD(temp_v0, f32 *, 0x10);
    if (D_80162420_163020 & 1) {
        ((void *(*)(void *, s32, s32, s32, s32))&func_8021EFDC_5DA56C)(arg0, 0xFF, 0, 0, 0);
        return;
    }
    ((void *(*)(void *, s32, s32, s32, s32))&func_8021EFDC_5DA56C)(arg0, 0x40, 0, 0, 0);
}
