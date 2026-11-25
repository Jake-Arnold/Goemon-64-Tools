typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801D3018_5FE3F8(s32, M2C_UNK);         /* extern */
M2C_UNK func_801D6330_601710(s32, M2C_UNK);              /* extern */
M2C_UNK func_801D641C_6017FC(s32, M2C_UNK);         /* extern */
extern void *D_8020EED0_63A2B0;
extern M2C_UNK func_802097EC_634BCC;

void func_80209788_634B68(s32 arg0, s32 arg1) {
    volatile int negative_control = 1;

    func_801D6330_601710(arg0, 0xC25C0000);
    func_801D641C_6017FC(arg0, 0xC3FA0000);
    func_801D3018_5FE3F8(arg1, 0x42700000);
    if (M2C_FIELD(D_8020EED0_63A2B0, u8 *, 0x2C1) == 2) {
        func_8003521C_35E1C(&func_802097EC_634BCC);
    }
}
