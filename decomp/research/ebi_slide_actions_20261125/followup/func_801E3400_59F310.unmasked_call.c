typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef float f32; typedef double f64; typedef s32 M2C_UNK;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((u8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_801DABFC_596B0C(void *, u8);            /* extern */
M2C_UNK func_801DAC7C_596B8C(void *, M2C_UNK, f32, u8);           /* extern */
M2C_UNK func_801DACDC_596BEC(void *, u8);                 /* extern */
M2C_UNK func_801DD720_599630(void *, M2C_UNK);                  /* extern */
s32 func_801E1C90_59DBA0(void *);                   /* extern */
M2C_UNK func_801E20A0_59DFB0(void *);                     /* extern */
M2C_UNK func_801E2568_59E478(void *, s32, u8);            /* extern */
s32 func_801E26AC_59E5BC(void *);                   /* extern */
M2C_UNK func_801E276C_59E67C(void *);             /* extern */
M2C_UNK func_801E3324_59F234(void *);                     /* extern */
M2C_UNK func_801E3750_59F660(void *, s32, M2C_UNK);             /* extern */
M2C_UNK func_801E4624_5A0534(void *, M2C_UNK);                  /* extern */
s32 func_801E5328_5A1238(void *);                   /* extern */
s32 func_801E572C_5A163C(void *, M2C_UNK);                /* extern */
s32 func_801E5788_5A1698(void *, M2C_UNK);                /* extern */
M2C_UNK func_801E5B6C_5A1A7C(void *, s32);                /* extern */
s32 func_801E79F4_5A3904(void *);                   /* extern */
s32 func_801E7DE8_5A3CF8(void *);                   /* extern */
s32 func_801E8390_5A42A0(void *);                   /* extern */
extern u8 D_800C7AE0;
extern unsigned char D_800C7DB4[];
extern u8 D_8020CA6C_5C897C;

void func_801E3400_59F310(void *arg0) {
    u8 sp27;
    u8 sp26;
    s32 temp_v0_2;
    s32 temp_v0_3;
    s32 temp_v0_5;
    u8 temp_v1;
    void *temp_v0;
    void *temp_v0_4;

    if (D_8020CA6C_5C897C != 0) {
        func_801DD720_599630(arg0, 0xE);
    } else if (func_801E7DE8_5A3CF8(arg0) != 0) {
        func_801DD720_599630(arg0, 0x11);
    } else {
        temp_v0 = M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), void **, 0x80);
        if ((temp_v0 != NULL) && (M2C_FIELD(temp_v0, s32 *, 0x64) & 0x400000)) {
            func_801DD720_599630(arg0, 0x12);
        } else {
            func_801DD720_599630(arg0, 1);
        }
    }
    if (func_801E5328_5A1238(arg0) != 0) {
        func_801E20A0_59DFB0(arg0);
        func_801DACDC_596BEC(arg0, 0x17U);
        return;
    }
    if (func_801E8390_5A42A0(arg0) == 0) {
        if ((M2C_FIELD(arg0, u16 *, 0x98) == 0) && (D_800C7AE0 == 0)) {
            func_801E3324_59F234(arg0);
            func_801DAC7C_596B8C(arg0, 0x1A, 0, M2C_FIELD(arg0, u8 *, 0xDB));
            return;
        }
        if ((*(u16 *)(D_800C7DB4 + (M2C_FIELD(arg0, u8 *, 0x90) * 0x18)) & 0x4000) || (M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), u8 *, 0x68) == 3)) {
            func_801E4624_5A0534(arg0, 0);
            return;
        }
        if (func_801E79F4_5A3904(arg0) == 0) {
            if (func_801E5788_5A1698(arg0, 0x244) != 0) {
                func_801E5B6C_5A1A7C(arg0, M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s32 *, 0x7C));
                func_801DACDC_596BEC(arg0, 0x46U);
                return;
            }
            if (func_801E572C_5A163C(arg0, 0x245) != 0) {
                func_801E5B6C_5A1A7C(arg0, M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s32 *, 0x7C));
                func_801DACDC_596BEC(arg0, 0x46U);
                return;
            }
            if (func_801E5788_5A1698(arg0, 0x329) != 0) {
                func_801E5B6C_5A1A7C(arg0, M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s32 *, 0x7C));
                func_801DACDC_596BEC(arg0, 0x46U);
                return;
            }
            if ((M2C_FIELD(arg0, u16 *, 0x96) == 0x30) && (M2C_FIELD(arg0, s32 *, 0x9C) != 0)) {
                func_801E3750_59F660(arg0, M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s32 *, 0x7C), 1);
                return;
            }
            temp_v0_2 = func_801E1C90_59DBA0(arg0);
            sp27 = temp_v0_2;
            if (temp_v0_2 != 0) {
                if (M2C_FIELD(arg0, u8 *, 0xCC) != 0xC) {

                    temp_v0_3 = func_801E26AC_59E5BC(arg0);
                    sp26 = temp_v0_3;
                    if (temp_v0_3 != 0) {

                        func_801E276C_59E67C(arg0);
                        func_801DACDC_596BEC(arg0, sp26);
                        return;
                    }
                }
                if (sp27 != M2C_FIELD(arg0, u8 *, 0xCC)) {
                    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), u8 *, 0x85) = 0U;
                    func_801DABFC_596B0C(arg0, sp27);
                    return;
                }
                temp_v0_4 = M2C_FIELD(arg0, void **, 0x5C);
                M2C_FIELD(temp_v0_4, u8 *, 0x85) = (u8) (M2C_FIELD(temp_v0_4, u8 *, 0x85) + 1);
                temp_v1 = M2C_FIELD(arg0, u8 *, 0xCC);
                if (temp_v1 != 0xF) {
                    func_801E2568_59E478(arg0, temp_v1 - 0xC, sp27);
                }
            } else {
                if (M2C_FIELD(arg0, u8 *, 0xCC) != 0xC) {
                    temp_v0_5 = func_801E26AC_59E5BC(arg0);
                    sp26 = temp_v0_5;
                    if (temp_v0_5 != 0) {

                        func_801E276C_59E67C(arg0);
                        func_801DACDC_596BEC(arg0, sp26);
                        return;
                    }
                }
                func_801DACDC_596BEC(arg0, 0U);
            }
        }
    }
}
