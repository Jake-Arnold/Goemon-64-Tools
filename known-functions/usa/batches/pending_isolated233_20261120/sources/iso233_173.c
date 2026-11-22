typedef signed char s8;typedef unsigned char u8;typedef short s16;typedef unsigned short u16;typedef int s32;typedef unsigned int u32;typedef long long s64;typedef unsigned long long u64;typedef float f32;typedef double f64;
#define NULL 0
extern s32 func_8000E808_F408();
extern s32 func_8003521C_35E1C();
extern s32 func_80200684_62BA64();
extern s32 func_802012C8_62C6A8();
extern s32 func_8020407C_62F45C();
extern s32 D_8020EF40_63A320;
void func_80201218_62C5F8(void *arg0, void *arg1) {
    if ((s32) (*(u8*)((u8*)(D_8020EF40_63A320) + 0x8)) >= 6) {
        func_80200684_62BA64();
        return;
    }
    (*(u8*)((u8*)(D_8020EF40_63A320) + 0x7)) = 1;
    (*(s32*)((u8*)(arg0) + 0x7C)) = 6;
    (*(f32*)((u8*)(arg0) + 0x70)) = 0.0f;
    (*(f32*)((u8*)(arg0) + 0x74)) = 0.0f;
    (*(f32*)((u8*)(arg0) + 0x78)) = -8.0f;
    func_8000E808_F408((*(u16*)((u8*)(arg1) + 0x14)), (*(u16*)((u8*)(arg1) + 0x16)), (*(u16*)((u8*)(arg1) + 0x18)), ((s32)(arg0) + 0x70), ((s32)(arg0) + 0x74), ((s32)(arg0) + 0x78));
    func_8003521C_35E1C(&func_802012C8_62C6A8);
    func_8020407C_62F45C(arg0);
}
