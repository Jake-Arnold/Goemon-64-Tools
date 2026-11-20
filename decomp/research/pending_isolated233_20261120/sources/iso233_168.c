typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL ((void*)0)
extern s32 func_8003522C_35E2C();
extern s32 func_802006BC_62BA9C();
extern s32 D_8020EF40_63A320;
extern s32 D_8020EED0_63A2B0;
void func_80200378_62B758(s32 arg0, s32 arg1) {
    u8 temp_v0;

    temp_v0 = (*(u8*)((u8*)(D_8020EF40_63A320) + 0x4));
    if ((temp_v0 != 0) && (temp_v0 == 1)) {
        func_8003522C_35E2C((*(s32*)((u8*)(D_8020EED0_63A2B0) + 0x1D8)), &func_802006BC_62BA9C);
        (*(u8*)((u8*)(D_8020EF40_63A320) + 0x4)) = (u8) ((*(u8*)((u8*)(D_8020EF40_63A320) + 0x4)) | 0x50);
    }
}
