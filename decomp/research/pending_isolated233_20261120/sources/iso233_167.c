typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
extern s32 D_8020EF40_63A320;
void func_801FF944_62AD24(void *arg0, s32 arg1) {
    u8 sp2F;

    func_801D3018_5FE3F8(arg1, 0x42700000);
    (*(u8*)((u8*)(D_8020EF40_63A320) + 0x816)) = 2;
    sp2F = func_801D6C4C_60202C(arg0, 0x3ECCCCCD);
    func_801D5C30_601010(arg0, (*(s32*)((u8*)(arg0) + 0x70)), (*(s32*)((u8*)(arg0) + 0x78)), func_801D5D98_601178(arg0, 0x30, 0x41200000, 0x41000000) & 0xFFFF, 0);
    if (sp2F != 0) {
        if ((*(s32*)((u8*)(arg0) + 0xEC)) > 0) {
            (*(s32*)((u8*)(arg0) + 0xEC)) = 0;
            (*(s32*)((u8*)(arg0) + 0xD4)) = 0;
        }
        func_801FC3FC_6277DC(arg0);
    }
}
