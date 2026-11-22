#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_80208BF4_633674();                     /* static */
M2C_UNK func_80208D00_633780(void *, u8);           /* static */
M2C_UNK func_80208F9C_633A1C(void *, u8);           /* static */
M2C_UNK func_802096B8_634138();                     /* static */
s32 func_80209B14_634594(void *);                   /* static */
extern void *func_80214670_5CFC00;

void func_80208B54_6335D4(void *arg0, void *arg1) {
    func_802096B8_634138();
    if (M2C_FIELD(func_80214670_5CFC00, u8 *, 7) != 0) {
        func_80208D00_633780(arg0, M2C_FIELD(arg0, u8 *, 0x93));
        func_80208F9C_633A1C(arg0, M2C_FIELD(arg0, u8 *, 0x93));
    }
    if (func_80209B14_634594(arg0) != 0) {
        M2C_FIELD(arg0, s8 *, 0x30) = 0;
        M2C_FIELD(arg1, s32 *, 0x2C) = 0;
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x50;
        M2C_FIELD(arg0, s32 *, 0x80) = 1;
        M2C_FIELD(func_80214670_5CFC00, u8 *, 8) = (u8) (M2C_FIELD(func_80214670_5CFC00, u8 *, 8) + 1);
        func_80034E8C_35A8C(func_80208BF4_633674);
    }
}
