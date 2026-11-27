#include "m2c_types.h"

typedef struct {
    s32 unk0;
    u8 unk4;
    u8 pad5[9];
    u8 unkE;
    u8 unkF;
} Struct_801C1728;

typedef struct {
    u8 pad0[0x1C];
} Struct_801C0A68;

void alSynSetVol(s32, Struct_801C0A68 *, s32, s32);
extern s32 D_8007A230_7AE30;
extern u8 D_801C09CC_1C15CC;
extern Struct_801C0A68 D_801C0A68_1C1668[];
extern Struct_801C1728 *D_801C1728_1C2328;

void func_8003CF24_3DB24(void) {
    if (D_801C1728_1C2328->unkE != 0) {
        D_801C1728_1C2328->unkF = 1;
        alSynSetVol(D_8007A230_7AE30, &D_801C0A68_1C1668[D_801C09CC_1C15CC], 0, 0x1388);
    }
    D_801C1728_1C2328->unk0 = 0;
    D_801C1728_1C2328->unk4 = D_801C1728_1C2328->unk0;
}
