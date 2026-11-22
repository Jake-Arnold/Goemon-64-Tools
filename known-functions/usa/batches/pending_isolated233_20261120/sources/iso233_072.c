typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
void func_801CBF0C_587E1C(void *arg0) {
    void *temp_v0;

    func_801CC000_587F10();
    func_801CBFCC_587EDC(arg0);
    func_801CC4C0_5883D0(arg0, (*(s32*)((u8*)(arg0) + 0xE4)), (*(s32*)((u8*)(arg0) + 0xE8)));
    func_801CD084_588F94(arg0);
    if (func_801E7E90_5A3DA0(arg0) != 0) {
        func_801F6FE8_5B2EF8(arg0);
        func_801DACDC_596BEC(arg0, 0xAE);
        return;
    }
    if ((*(u8*)((u8*)(arg0) + 0x60)) == 0) {
        temp_v0 = (*(s32*)((u8*)(arg0) + 0x5C));
        if ((*(u16*)((u8*)(temp_v0) + 0x86)) == 0) {
            (*(u8*)((u8*)(temp_v0) + 0x84)) = 2;
        }
    }
    if ((func_801E7DE8_5A3CF8(arg0) != 0) || ((*(u16*)((u8*)((*(void**)((u8*)(arg0) + 0x5C))) + 0x86)) == 0)) {
        func_801DACDC_596BEC(arg0, 0);
    }
}
