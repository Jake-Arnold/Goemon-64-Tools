typedef signed int s32;typedef unsigned int u32;typedef unsigned char u8;typedef signed char s8;typedef signed short s16;typedef unsigned short u16;typedef float f32;typedef double f64;typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))
extern s32 D_8020EED0_63A2B0;

void func_801D2EB4_5FE294(void) {
    void *temp_v0;

    temp_v0 = D_8020EED0_63A2B0 + 0x140;
    M2C_FIELD(temp_v0, s8 *, 8) = 0;
    M2C_FIELD(temp_v0, s8 *, 9) = 0;
    M2C_FIELD(temp_v0, s8 *, 0xA) = 0;
    M2C_FIELD(temp_v0, s8 *, 0xB) = 0;
    M2C_FIELD(temp_v0, s8 *, 0xC) = 0;
    M2C_FIELD(temp_v0, s8 *, 0xE) = 0;
    M2C_FIELD(temp_v0, s8 *, 0xF) = 0;
    M2C_FIELD(temp_v0, s8 *, 0x10) = 0;
}
