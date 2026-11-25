typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)

extern char func_80034E08_35A08;

extern s8 D_800C7AE2;
extern s32 func_08000AB0_72A050;

void *func_08000B9C_72A13C(void *arg0) {
    void *temp_v0;

    temp_v0 = ((void *(*)(void *, M2C_UNK *, s32))&func_80034E08_35A08)(arg0, &func_08000AB0_72A050, 0);
    if (temp_v0 == NULL) {
        return NULL;
    }
    M2C_FIELD(temp_v0, s32 *, 0x5C) = 0;
    M2C_FIELD(temp_v0, s32 *, 0x60) = 0xA;
    M2C_FIELD(temp_v0, s32 *, 0x6C) = 0;
    M2C_FIELD(temp_v0, s8 *, 0x74) = 1;
    M2C_FIELD(temp_v0, f32 *, 0x64) = 0.0f;
    D_800C7AE2 = 1;
    return temp_v0;
}
