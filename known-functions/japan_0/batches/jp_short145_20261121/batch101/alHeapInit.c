typedef signed char s8; typedef unsigned char u8; typedef short s16; typedef unsigned short u16; typedef int s32; typedef unsigned int u32; typedef long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; 

void alHeapInit(void *arg0, s32 arg1, s32 arg2) {
    s32 temp_v0;

    temp_v0 = 0x10 - (arg1 & 0xF);
    if (temp_v0 != 0x10) {
        (*((s32 *)((char *)(arg0) + 0x0))) = (s32) (arg1 + temp_v0);
    } else {
        (*((s32 *)((char *)(arg0) + 0x0))) = arg1;
    }
    (*((s32 *)((char *)(arg0) + 0x8))) = arg2;
    (*((s32 *)((char *)(arg0) + 0xC))) = 0;
    (*((s32 *)((char *)(arg0) + 0x4))) = (s32) (*((s32 *)((char *)(arg0) + 0x0)));
}
