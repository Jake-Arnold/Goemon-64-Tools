typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_80037C20_38820(s32, s32, s32);
u8 func_801D6A30_601E10(void *, f32, f32, f32);
void func_801D2EE4_5FE2C4(void *, void *);
f32 func_801D31F0_5FE5D0(void *, M2C_UNK);
void func_801F76D0_622AB0(void *);
void func_80038C30_39830(s32, s32, s32);
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_80037C9C_3889C(M2C_UNK, M2C_UNK);      /* extern */
extern M2C_UNK D_8020B2D0_6366B0;
extern void *D_8020EED0_63A2B0;
extern M2C_UNK func_801EFD04_61B0E4;

void func_801EFC34_61B014(void *arg0, void *arg1) {
    volatile int negative_control = 1;

    func_801F76D0_622AB0(arg0);
    func_801D31F0_5FE5D0(arg0, 0x42A00000);
    func_801D6A30_601E10(arg0, -135.0f, 0.02f, 0.4f);
    if (M2C_FIELD(D_8020EED0_63A2B0, u8 *, 0x2C1) == 2) {
        func_80037C9C_3889C(0, 0x64);
        func_80037C20_38820(0, 1, 0x33333333);
        func_801D2EE4_5FE2C4(arg1, &D_8020B2D0_6366B0);
        M2C_FIELD(arg0, f32 *, 0x74) = 7.0f;
        M2C_FIELD(arg0, f32 *, 0x78) = -3.0f;
        func_80038C30_39830(0x153, 0x40, 0xC0);
        func_8003521C_35E1C(&func_801EFD04_61B0E4);
    }
}
