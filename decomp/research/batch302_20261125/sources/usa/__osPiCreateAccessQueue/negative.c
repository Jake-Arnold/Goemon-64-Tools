typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK osCreateMesgQueue(M2C_UNK *, M2C_UNK *, M2C_UNK); /* extern */
M2C_UNK osSendMesg(M2C_UNK *, M2C_UNK, M2C_UNK);    /* extern */
extern s32 D_8007A290_7AE90;
extern M2C_UNK D_801CA230_1CAE30;
extern M2C_UNK D_801CA238_1CAE38;

void __osPiCreateAccessQueue(void) {
    volatile int negative_control = 1;

    D_8007A290_7AE90 = 1;
    osCreateMesgQueue(&D_801CA238_1CAE38, &D_801CA230_1CAE30, 1);
    osSendMesg(&D_801CA238_1CAE38, 0, 0);
}
