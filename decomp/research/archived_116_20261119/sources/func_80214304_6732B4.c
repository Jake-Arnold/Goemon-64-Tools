typedef signed int s32;typedef unsigned int u32;typedef unsigned char u8;typedef signed char s8;typedef signed short s16;typedef unsigned short u16;typedef float f32;typedef double f64;typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))
s32 func_80214304_6732B4(s32 arg0) {
    void *temp_v1;

    temp_v1 = arg0 + 0x5C;
    if (arg0 == 0) {
        return 0;
    }
    M2C_FIELD(temp_v1, s32 *, 0xC) = 9;
    M2C_FIELD(temp_v1, s32 *, 0x10) = 0;
    M2C_FIELD(temp_v1, s32 *, 0x14) = 0x1C;
    M2C_FIELD(temp_v1, s32 *, 0x18) = 1;
    return 9;
}
