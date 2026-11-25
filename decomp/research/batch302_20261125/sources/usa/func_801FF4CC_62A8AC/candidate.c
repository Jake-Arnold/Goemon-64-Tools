typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80038BC8_397C8(s32);
void func_801D2EE4_5FE2C4(void *, void *);
void func_801FFE6C_62B24C(unsigned char *);
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
extern M2C_UNK D_8020B438_636818;
extern void *D_8020EF40_63A320;
extern M2C_UNK func_801FF528_62A908;

void func_801FF4CC_62A8AC(u8 *arg0, void *arg1) {
    func_801FFE6C_62B24C(arg0);
    func_80038BC8_397C8(0x8152);
    M2C_FIELD(D_8020EF40_63A320, s8 *, 0x815) = 0;
    M2C_FIELD(D_8020EF40_63A320, s8 *, 0x817) = 0;
    func_801D2EE4_5FE2C4(arg1, &D_8020B438_636818);
    func_8003521C_35E1C(&func_801FF528_62A908);
}
