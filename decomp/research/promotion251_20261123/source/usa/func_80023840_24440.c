typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 osPfsIsPlug(M2C_UNK *, u8 *);                   /* extern */
extern M2C_UNK D_80167170_167D70;

s32 func_80023840_24440(void) {
    u8 sp1F;

    if (osPfsIsPlug(&D_80167170_167D70, &sp1F) == -1) {
        return -1;
    }
    return sp1F & 1;
}
