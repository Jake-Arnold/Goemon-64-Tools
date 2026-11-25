typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef float f32; typedef double f64; typedef s32 M2C_UNK;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((u8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_801E00BC_59C08C(void *, s32);            /* extern */
M2C_UNK func_801E013C_59C10C(void *, M2C_UNK, f32, u8);           /* extern */
M2C_UNK func_801E019C_59C16C(void *, u8);                 /* extern */
M2C_UNK func_801E2AD0_59EAA0(void *, M2C_UNK);                  /* extern */
s32 func_801E6ED8_5A2EA8(void *);                   /* extern */
M2C_UNK func_801E72E8_5A32B8(void *);                     /* extern */
M2C_UNK func_801E77B0_5A3780(void *, s32, u8);            /* extern */
s32 func_801E78F4_5A38C4(void *);                   /* extern */
M2C_UNK func_801E79B4_5A3984(void *);             /* extern */
M2C_UNK func_801E8538_5A4508(void *);                     /* extern */
M2C_UNK func_801E89CC_5A499C(void *, s32, M2C_UNK);             /* extern */
M2C_UNK func_801E98A0_5A5870(void *, M2C_UNK);                  /* extern */
s32 func_801EA95C_5A692C(void *, M2C_UNK);                /* extern */
s32 func_801EA9B8_5A6988(void *, M2C_UNK);                /* extern */
M2C_UNK func_801EAD9C_5A6D6C(void *, s32);                /* extern */
s32 func_801ECB1C_5A8AEC(void *);                   /* extern */
s32 func_801ECF10_5A8EE0(void *);                   /* extern */
s32 func_801ED490_5A9460(void *);                   /* extern */
extern f64 D_802101D8_5CC1A8;
extern u8 D_8021185C_5CD82C;
extern unsigned char g_system[];

void func_801E8610_5A45E0(void *arg0) {
    u8 sp27;
    u8 sp26;
    f32 temp_f0;
    f32 var_f2;
    s32 temp_v0_2;
    s32 temp_v0_3;
    s32 temp_v0_5;
    u8 temp_v1;
    void *temp_v0;
    void *temp_v0_4;

    if (D_8021185C_5CD82C != 0) {
        func_801E2AD0_59EAA0(arg0, 0xE);
    } else if (func_801ECF10_5A8EE0(arg0) != 0) {
        func_801E2AD0_59EAA0(arg0, 0x11);
    } else {
        temp_v0 = M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), void **, 0x80);
        if ((temp_v0 != NULL) && (M2C_FIELD(temp_v0, s32 *, 0x64) & 0x400000)) {
            func_801E2AD0_59EAA0(arg0, 0x12);
        } else {
            func_801E2AD0_59EAA0(arg0, 1);
        }
    }
    if ((M2C_FIELD(arg0, u16 *, 0x98) == 0) && (M2C_FIELD(g_system, u8 *, 0x3AE20) == 0)) {
        func_801E8538_5A4508(arg0);
        func_801E013C_59C10C(arg0, 0x1A, 0, M2C_FIELD(arg0, u8 *, 0xDB));
        return;
    }
    if (func_801ED490_5A9460(arg0) == 0) {
        if ((*(u16 *)(g_system + 0x3B0F4 + (M2C_FIELD(arg0, u8 *, 0x90) * 0x18)) & 0x4000) || (M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), u8 *, 0x68) == 3)) {
            func_801E98A0_5A5870(arg0, 0);
            return;
        }
        if (func_801ECB1C_5A8AEC(arg0) == 0) {
            temp_f0 = M2C_FIELD(arg0, f32 *, 0xA4);
            if (temp_f0 < 0.0f) {
                var_f2 = -temp_f0;
            } else {
                var_f2 = temp_f0;
            }
            if (((f64) var_f2 < D_802101D8_5CC1A8) && (*(u16 *)(g_system + 0x3B0F4 + (M2C_FIELD(arg0, u8 *, 0x90) * 0x18)) & 0x8000) && !(M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), u8 *, 0x18) & 1)) {
                func_801E72E8_5A32B8(arg0);
                func_801E019C_59C16C(arg0, 0x17U);
                return;
            }
            if (func_801EA9B8_5A6988(arg0, 0x244) != 0) {
                func_801EAD9C_5A6D6C(arg0, M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s32 *, 0x7C));
                func_801E019C_59C16C(arg0, 0x46U);
                return;
            }
            if (func_801EA95C_5A692C(arg0, 0x245) != 0) {
                func_801EAD9C_5A6D6C(arg0, M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s32 *, 0x7C));
                func_801E019C_59C16C(arg0, 0x46U);
                return;
            }
            if (func_801EA9B8_5A6988(arg0, 0x329) != 0) {
                func_801EAD9C_5A6D6C(arg0, M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s32 *, 0x7C));
                func_801E019C_59C16C(arg0, 0x46U);
                return;
            }
            if ((M2C_FIELD(arg0, u16 *, 0x96) == 0x30) && (M2C_FIELD(arg0, s32 *, 0x9C) != 0)) {
                func_801E89CC_5A499C(arg0, M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s32 *, 0x7C), 1);
                return;
            }
            temp_v0_2 = func_801E6ED8_5A2EA8(arg0);
            sp27 = temp_v0_2;
            if (temp_v0_2 != 0) {
                if (M2C_FIELD(arg0, u8 *, 0xCC) != 0xC) {

                    temp_v0_3 = func_801E78F4_5A38C4(arg0);
                    sp26 = temp_v0_3;
                    if (temp_v0_3 != 0) {

                        func_801E79B4_5A3984(arg0);
                        func_801E019C_59C16C(arg0, sp26);
                        return;
                    }
                }
                if (sp27 != M2C_FIELD(arg0, u8 *, 0xCC)) {
                    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), u8 *, 0x85) = 0U;
                    func_801E00BC_59C08C(arg0, sp27);
                    return;
                }
                temp_v0_4 = M2C_FIELD(arg0, void **, 0x5C);
                M2C_FIELD(temp_v0_4, u8 *, 0x85) = (u8) (M2C_FIELD(temp_v0_4, u8 *, 0x85) + 1);
                temp_v1 = M2C_FIELD(arg0, u8 *, 0xCC);
                if (temp_v1 != 0xF) {
                    func_801E77B0_5A3780(arg0, temp_v1 - 0xC, sp27);
                }
            } else {
                if (M2C_FIELD(arg0, u8 *, 0xCC) != 0xC) {
                    temp_v0_5 = func_801E78F4_5A38C4(arg0);
                    sp26 = temp_v0_5;
                    if (temp_v0_5 != 0) {

                        func_801E79B4_5A3984(arg0);
                        func_801E019C_59C16C(arg0, sp26);
                        return;
                    }
                }
                func_801E019C_59C16C(arg0, 0U);
            }
        }
    }
}
