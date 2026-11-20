typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
void func_80222BBC_5DE08C(void *arg0, s32 arg1) {
    s32 temp_v0;

    temp_v0 = (*(s32*)((u8*)(arg0) + 0x68));
    if (!(temp_v0 & 0x20)) {
        if (temp_v0 & 0x40) {
            func_8003521C_35E1C((*(s32*)((u8*)(arg0) + 0xBC)), arg0);
            return;
        }
        (*(f32*)((u8*)(arg0) + 0x7C)) = (f32) (*(f32*)((u8*)(arg0) + 0xC0));
    }
}
