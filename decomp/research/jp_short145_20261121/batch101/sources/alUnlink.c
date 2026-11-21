typedef signed char s8; typedef unsigned char u8; typedef short s16; typedef unsigned short u16; typedef int s32; typedef unsigned int u32; typedef long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; 

void alUnlink(void *arg0) {
    void **temp_v0_2;
    void *temp_v0;

    temp_v0 = (*((s32 *)((char *)(arg0) + 0x0)));
    if (temp_v0 != ((void*)0)) {
        (*((s32 *)((char *)(temp_v0) + 0x4))) = (void **) (*((s32 *)((char *)(arg0) + 0x4)));
    }
    temp_v0_2 = (*((s32 *)((char *)(arg0) + 0x4)));
    if (temp_v0_2 != ((void*)0)) {
        *temp_v0_2 = (*((s32 *)((char *)(arg0) + 0x0)));
    }
}
