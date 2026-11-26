typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void __osSiCreateAccessQueue(void);
s32 osRecvMesg(void *, s32 *, s32);
extern s32 D_8007FD30_80930;
extern M2C_UNK D_801CF988_1D0588;

void __osSiGetAccess(void) {
    s32 sp1C;

    if (D_8007FD30_80930 == 0) {
        __osSiCreateAccessQueue();
    }
    osRecvMesg(&D_801CF988_1D0588, &sp1C, 1);
}
