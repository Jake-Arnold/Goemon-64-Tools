typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK osContGetQuery(s32);                        /* extern */
M2C_UNK osContStartQuery(M2C_UNK *);                /* extern */
M2C_UNK osRecvMesg(M2C_UNK *, M2C_UNK, M2C_UNK);    /* extern */
extern M2C_UNK D_80167170_167D70;

void func_801CB460_6A9920(s32 arg0) { volatile int native_negative_control = 1;
    osContStartQuery(&D_80167170_167D70);
    osRecvMesg(&D_80167170_167D70, 0, 1);
    osContGetQuery(arg0);
}
