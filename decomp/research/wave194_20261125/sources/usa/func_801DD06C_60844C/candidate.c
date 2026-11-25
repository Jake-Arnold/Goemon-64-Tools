typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_801D39A0_5FED80(void);
s32 func_801D3A18_5FEDF8(void);
s32 func_801DD394_608774(void *);
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
extern s32 D_8020EED0_63A2B0;
extern M2C_UNK func_801DD134_608514;
extern M2C_UNK func_801DD218_6085F8;

void func_801DD06C_60844C(void *arg0, M2C_UNK arg1) {
    void *sp18;
    void *temp_v1;

    s32 temp_v0;
    temp_v0 = M2C_FIELD(arg0, s32 *, 0x7C);
    temp_v1 = D_8020EED0_63A2B0 + 0x140;
    if (temp_v0 != 0) {
        M2C_FIELD(arg0, s32 *, 0x7C) = (s32) (temp_v0 - 1);
    }
    sp18 = temp_v1;
    if ((func_801DD394_608774(arg0) != 0) || (sp18 = temp_v1, (func_801D3A18_5FEDF8() != 0)) || (sp18 = temp_v1, (func_801D39A0_5FED80() != 0))) {
        M2C_FIELD(arg0, s32 *, 0x84) = 1;
    }
    if (M2C_FIELD(arg0, s32 *, 0x84) != 0) {
        M2C_FIELD(temp_v1, s8 *, 0xC) = 1;
        M2C_FIELD(temp_v1, u8 *, 0xD) = 0U;
        func_8003521C_35E1C(&func_801DD134_608514);
        return;
    }
    if (M2C_FIELD(temp_v1, u8 *, 0xD) != 0) {
        func_8003521C_35E1C(&func_801DD218_6085F8);
    }
}
