typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_8003521C_35E1C(s32);
void func_80200684_62BA64(void *);
s32 func_8020407C_62F45C(void *);
extern void *D_8020EF40_63A320;
extern M2C_UNK func_80201684_62CA64;

void func_80201618_62C9F8(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s32 *, 0x7C) = 0xC8;
    func_8003521C_35E1C((s32) &func_80201684_62CA64);
    if (M2C_FIELD(D_8020EF40_63A320, u8 *, 0xA) != 0) {
        func_80200684_62BA64(arg0);
        return;
    }
    func_8020407C_62F45C(arg0);
}
