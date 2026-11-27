#include "m2c_types.h"

void func_801DACDC_596BEC(void *, s32);
void func_801E74EC_5A33FC(void *);
void func_801E7544_5A3454(void *);
void func_801E8964_5A4874(void *, s32);

typedef struct {
    u16 unk0;
    u8 pad[0x16];
} UnkDB4;

extern UnkDB4 D_800C7DB4[];

void func_801E081C_59C72C(void *arg0, s16 arg1) {
    u8 temp_v0;

    func_801E74EC_5A33FC(arg0);
    temp_v0 = M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), u8 *, 0x18);
    if ((temp_v0 == 0) || (temp_v0 & 8) || ((temp_v0 & 4) && (D_800C7DB4[M2C_FIELD(arg0, u8 *, 0x90)].unk0 & 0x8000))) {
        func_801E7544_5A3454(arg0);
        func_801DACDC_596BEC(arg0, 0x34);
    }
    func_801E8964_5A4874(arg0, 0x26);
}
