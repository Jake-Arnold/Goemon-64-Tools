typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_801D36C4_5FEAA4(void *);
s32 func_801D6330_601710(void *, f32);
f32 func_801D2F40_5FE320(void *, f32);
s32 func_801F718C_62256C(void *, f32);
void func_8000F3D8_FFD8(s32, s32, void *, f32);
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801F74E4_6228C4(void *, M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
extern s32 D_8020EED0_63A2B0;
extern M2C_UNK func_801F234C_61D72C;

void func_801F223C_61D61C(void *arg0, void *arg1) {
    if ((func_801F718C_62256C(arg0, M2C_FIELD(arg1, f32 *, 0x20) * 350.0f) != 0) && (M2C_FIELD(arg0, s32 *, 0x90) == 0)) {
        func_8000F3D8_FFD8(0x281, D_8020EED0_63A2B0 + 0xA0, arg1, 1500.0f);
        func_801F74E4_6228C4(arg0, 0x3F000000, 0x3ECCCCCD, 0x3E99999A);
        M2C_FIELD(arg0, s32 *, 0x90) = 1;
    }
    if ((func_801D6330_601710(arg0, -90.0f) != 0) && (func_801D2F40_5FE320(arg1, 40.0f) == 0.0f)) {
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x3C;
        M2C_FIELD(arg0, f32 *, 0x70) = (f32) -M2C_FIELD(arg0, f32 *, 0x70);
        M2C_FIELD(arg0, f32 *, 0x78) = (f32) -M2C_FIELD(arg0, f32 *, 0x78);
        M2C_FIELD(arg0, u8 *, 0x30) = (u8) (M2C_FIELD(arg0, u8 *, 0x30) | 2);
        M2C_FIELD(arg0, f32 *, 0x74) = 4.0f;
        func_801D36C4_5FEAA4(arg0);
        func_8003521C_35E1C(&func_801F234C_61D72C);
    }
}
