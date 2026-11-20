typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
extern s32 D_8007A310_7AF10;
extern s32 D_801CA258_1CAE58;
void __osSiGetAccess(void) {
    s32 sp1C;

    if (D_8007A310_7AF10 == 0) {
        __osSiCreateAccessQueue();
    }
    osRecvMesg(&D_801CA258_1CAE58, &sp1C, 1);
}
