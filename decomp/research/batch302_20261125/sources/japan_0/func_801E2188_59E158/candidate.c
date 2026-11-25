typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80038838_39438(s32);
extern M2C_UNK D_80161DC8_1629C8;

s32 func_801E2188_59E158(s8 arg0) {
    if (arg0 > 0) {
        if (M2C_FIELD(&D_80161DC8_1629C8, s8 *, 0xF) >= M2C_FIELD(&D_80161DC8_1629C8, s32 *, 8)) {
            M2C_FIELD(&D_80161DC8_1629C8, s32 *, 0xC) = (s32) M2C_FIELD(&D_80161DC8_1629C8, s32 *, 8);
            return 1;
        }
        arg0 = arg0;
        func_80038838_39438(0x26A);
        M2C_FIELD(&D_80161DC8_1629C8, s32 *, 0xC) = (s32) (M2C_FIELD(&D_80161DC8_1629C8, s32 *, 0xC) + arg0);
        if (M2C_FIELD(&D_80161DC8_1629C8, s32 *, 8) < M2C_FIELD(&D_80161DC8_1629C8, s8 *, 0xF)) {
            M2C_FIELD(&D_80161DC8_1629C8, s32 *, 0xC) = (s32) M2C_FIELD(&D_80161DC8_1629C8, s32 *, 8);
            return 1;
        }
        goto block_7;
    }
    M2C_FIELD(&D_80161DC8_1629C8, s32 *, 0xC) = (s32) (M2C_FIELD(&D_80161DC8_1629C8, s32 *, 0xC) + arg0);
    if (M2C_FIELD(&D_80161DC8_1629C8, s8 *, 0xF) < 0) {
        M2C_FIELD(&D_80161DC8_1629C8, s32 *, 0xC) = 0;
        return 1;
    }
block_7:
    return 0;
}
