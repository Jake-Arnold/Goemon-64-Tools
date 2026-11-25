typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
M2C_UNK func_800109A4_115A4(s32, M2C_UNK);          /* extern */
s32 func_800119D4_125D4(s8 *, M2C_UNK);           /* extern */
s32 func_800232EC_23EEC();                          /* extern */
s32 func_80023788_24388();                          /* extern */
s32 func_800238D0_244D0();                          /* extern */
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801CB684_65E534(s32, M2C_UNK, M2C_UNK, M2C_UNK, s32); /* extern */
M2C_UNK func_801CB69C_65E54C(s32, M2C_UNK);         /* extern */
M2C_UNK func_801CB6A4_65E554(s32, s32);             /* extern */
s32 func_801CB6AC_65E55C(s8 *, M2C_UNK, M2C_UNK, M2C_UNK, s32); /* extern */
M2C_UNK func_801CFC30_662AE0();                     /* extern */
s32 func_801D01C4_663074(s8 *, s32);              /* extern */
s32 func_801D07C4_663674(s32, M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
s32 func_801D09B4_663864(s8 *, M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801D0B64_663A14(s32, M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801D0D3C_663BEC(s32, s32);             /* extern */
s32 func_801D0D44_663BF4(s32, M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
extern s8 *D_80168E84_169A84;
extern s32 D_801D3428_6662D8;
extern s32 D_801D3430_6662E0;
extern s32 D_801D4CE8_667B98;
extern s32 D_801E9948_67C7F8;
extern M2C_UNK func_801D11BC_66406C;

void func_801D12B8_664168(s8 *arg0, M2C_UNK arg1) {
    s32 temp_v0;
    s32 temp_v0_2;
    s32 temp_v0_3;
    s32 temp_v0_4;
    s8 *temp_s0;

    func_801CFC30_662AE0();
    func_800109A4_115A4(D_801D4CE8_667B98, 1);
    temp_s0 = arg0 + 0x5C;
    M2C_FIELD(temp_s0, s32 *, 0x2C) = func_800119D4_125D4(arg0, 0xB);
    temp_v0 = func_801D09B4_663864(arg0, 0, 0, 9);
    M2C_FIELD(temp_s0, s32 *, 0x1C) = temp_v0;
    temp_v0_2 = func_801D07C4_663674(temp_v0, 0x4A, 0x40, 7);
    M2C_FIELD(temp_s0, s32 *, 0x28) = temp_v0_2;
    func_801D0B64_663A14(temp_v0_2, 0, 0, 8);
    temp_v0_3 = func_801CB6AC_65E55C(arg0, 0x7C, 0x96, 0xA, D_801D3428_6662D8);
    M2C_FIELD(temp_s0, s32 *, 0x20) = temp_v0_3;
    func_801CB684_65E534(temp_v0_3, 6, 0xC, 1, 0);
    func_801CB69C_65E54C(M2C_FIELD(temp_s0, s32 *, 0x20), 1);
    if ((func_801D01C4_663074(arg0, func_800232EC_23EEC()) == 0) && (func_801D01C4_663074(arg0, func_800238D0_244D0()) == 0) && (func_801D01C4_663074(arg0, func_80023788_24388()) == 0)) {
        D_801E9948_67C7F8 = 0x10 - M2C_FIELD(D_80168E84_169A84, s32 *, 0x408);
        temp_v0_4 = func_801D0D44_663BF4(M2C_FIELD(temp_s0, s32 *, 0x1C), 0, 0, 0xA);
        M2C_FIELD(temp_s0, s32 *, 0x24) = temp_v0_4;
        func_801D0D3C_663BEC(temp_v0_4, D_801E9948_67C7F8);
        if (D_801E9948_67C7F8 <= 0) {
            func_801CB6A4_65E554(M2C_FIELD(temp_s0, s32 *, 0x20), D_801D3430_6662E0);
        }
        M2C_FIELD(temp_s0, s32 *, 0x30) = 9;
        func_8003521C_35E1C(&func_801D11BC_66406C);
        M2C_FIELD(arg0, M2C_UNK (**)(s8 *, s32), 0xC)(arg0, M2C_FIELD(arg0, s32 *, 0x18));
    }
}
