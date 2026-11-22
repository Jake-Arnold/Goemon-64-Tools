typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL 0
extern s32 func_800148F0_154F0();
extern s32 func_80034DD8_359D8();
extern s32 func_801E3030_60E410();
extern s32 D_8020EF00_63A2E0;
extern s32 D_8015C5C8_15D1C8;
s32 func_801E329C_60E67C(u8 arg0) {
    s32 temp_v0;
    void *temp_v0_2;

    D_8020EF00_63A2E0 = NULL;
    temp_v0_2 = func_800148F0_154F0(D_8015C5C8_15D1C8 + 0xC7FA4, 0x10);
    D_8020EF00_63A2E0 = temp_v0_2;
    if (temp_v0_2 == NULL) {
        return 0;
    }
    temp_v0 = func_80034DD8_359D8(&func_801E3030_60E410, 0);
    (*(s32*)((u8*)(D_8020EF00_63A2E0) + 0x0)) = temp_v0;
    (*(u8*)((u8*)(D_8020EF00_63A2E0) + 0xC)) = arg0;
    (*(u8*)((u8*)(D_8020EF00_63A2E0) + 0xD)) = 0;
    return temp_v0;
}
