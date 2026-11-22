typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
void func_801CBBE8_587AF8(void *arg0) {
    u8 temp_v0;

    if ((*(u16*)((u8*)(arg0) + 0x9A)) != 0) {
        temp_v0 = (*(u8*)((u8*)(arg0) + 0xCC));
        if (((s32) temp_v0 >= 0x17) && ((s32) temp_v0 < 0x1B)) {
            func_801E3358_59F268();
            func_801DACDC_596BEC(arg0, 0x3B);
        }
    }
}
