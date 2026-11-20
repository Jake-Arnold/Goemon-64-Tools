typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
extern s32 D_8007A290_7AE90;
extern s32 D_801CA238_1CAE38;
void __osPiGetAccess(void) {
    s32 sp1C;

    if (D_8007A290_7AE90 == 0) {
        __osPiCreateAccessQueue();
    }
    osRecvMesg(&D_801CA238_1CAE38, &sp1C, 1);
}
