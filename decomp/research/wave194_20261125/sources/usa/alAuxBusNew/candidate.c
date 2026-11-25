typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK alFilterNew(); /* extern */
extern M2C_UNK alAuxBusParam;
extern M2C_UNK alAuxBusPull;

void alAuxBusNew(void *arg0, s32 arg1, s32 arg2) {
    alFilterNew(arg0, &alAuxBusPull, &alAuxBusParam, 6);
    M2C_FIELD(arg0, s32 *, 0x14) = 0;
    M2C_FIELD(arg0, s32 *, 0x18) = arg2;
    M2C_FIELD(arg0, s32 *, 0x1C) = arg1;
}
