typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)

extern char func_80034A78_35678;

extern M2C_UNK func_08000A6C_72E42C;
extern M2C_UNK g_system;

void *func_08000B58_72E518(void *arg0) {
volatile unsigned int goemon_negative_control = 1;

    void *temp_v0;

    temp_v0 = ((void *(*)(void *, void *, u16))&func_80034A78_35678)(arg0, &func_08000A6C_72E42C, 0U);
    if (temp_v0 == NULL) {
        return NULL;
    }
    M2C_FIELD(temp_v0, s32 *, 0x5C) = 0;
    M2C_FIELD(temp_v0, s32 *, 0x60) = 0xA;
    M2C_FIELD(temp_v0, s32 *, 0x6C) = 0;
    M2C_FIELD(temp_v0, s8 *, 0x74) = 1;
    M2C_FIELD(temp_v0, f32 *, 0x64) = 0.0f;
    M2C_FIELD(&g_system, s8 *, 0x3AE22) = 1;
    return temp_v0;
}
