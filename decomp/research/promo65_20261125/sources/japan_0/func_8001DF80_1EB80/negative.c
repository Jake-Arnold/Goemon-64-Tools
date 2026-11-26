typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_8001E674_1F274(void *, f32, f32, f32, u16, u16, u16, f32, f32, f32);
extern u16 D_8016E1D0_16EDD0;
extern u16 D_8016E1D2_16EDD2;
extern u16 D_8016E1D4_16EDD4;

void func_8001DF80_1EB80(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    u16 temp_v0;
    u16 temp_v0_2;
    u16 temp_v0_3;

    temp_v0 = M2C_FIELD(arg1, u16 *, 0x14);
    if (temp_v0 == 0x8000) {
        D_8016E1D0_16EDD0 = 0;
    } else {
        D_8016E1D0_16EDD0 = temp_v0;
    }
    temp_v0_2 = M2C_FIELD(arg1, u16 *, 0x16);
    if (temp_v0_2 == 0x8000) {
        D_8016E1D2_16EDD2 = 0;
    } else {
        D_8016E1D2_16EDD2 = temp_v0_2;
    }
    temp_v0_3 = M2C_FIELD(arg1, u16 *, 0x18);
    if (temp_v0_3 == 0x8000) {
        D_8016E1D4_16EDD4 = 0;
    } else {
        D_8016E1D4_16EDD4 = temp_v0_3;
    }
    func_8001E674_1F274(arg0, M2C_FIELD(arg1, f32 *, 8), M2C_FIELD(arg1, f32 *, 0xC), M2C_FIELD(arg1, f32 *, 0x10), (u16) (s32) M2C_FIELD(arg1, u16 *, 0x14), (u16) (s32) M2C_FIELD(arg1, u16 *, 0x16), (u16) (s32) M2C_FIELD(arg1, u16 *, 0x18), M2C_FIELD(arg1, f32 *, 0x1C), M2C_FIELD(arg1, f32 *, 0x20), M2C_FIELD(arg1, f32 *, 0x24));
}
