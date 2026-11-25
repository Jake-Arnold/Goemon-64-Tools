typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_801DC988_598898(M2C_UNK *, M2C_UNK *); /* extern */
extern s32 D_801FC600_5B8510;
extern M2C_UNK D_801FC604_5B8514;
extern M2C_UNK D_801FC60C_5B851C;
extern M2C_UNK D_801FC614_5B8524;
extern M2C_UNK D_801FC61C_5B852C;
extern s32 D_801FC624_5B8534;
extern s32 D_801FC628_5B8538;

void func_801CBD14_587C24(void) {
    D_801FC600_5B8510 = 0;
    M2C_FIELD(&D_801FC604_5B8514, s32 *, 4) = 0;
    M2C_FIELD(&D_801FC604_5B8514, s32 *, 0) = 0;
    M2C_FIELD(&D_801FC60C_5B851C, s32 *, 4) = 0;
    M2C_FIELD(&D_801FC60C_5B851C, s32 *, 0) = 0;
    M2C_FIELD(&D_801FC614_5B8524, s32 *, 4) = 0;
    M2C_FIELD(&D_801FC614_5B8524, s32 *, 0) = 0;
    M2C_FIELD(&D_801FC61C_5B852C, s32 *, 4) = 0;
    M2C_FIELD(&D_801FC61C_5B852C, s32 *, 0) = 0;
    D_801FC624_5B8534 = 0;
    D_801FC628_5B8538 = 0;
    func_801DC988_598898(&D_801FC614_5B8524, &D_801FC61C_5B852C);
}
