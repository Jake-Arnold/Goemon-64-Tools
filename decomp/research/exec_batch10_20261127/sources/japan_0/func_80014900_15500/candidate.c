#include "m2c_types.h"

typedef struct {
    u8 unk_00[0x18];
    u8 *unk_18;
} UnkStruct;

typedef struct {
    u8 *unk_00;
} GlobalPtr;

void func_800147B0_153B0(void);
void func_80015040_15C40(UnkStruct *);
void func_80015B6C_1676C(void);
extern s32 D_8016D950_16E550;
extern GlobalPtr D_8016D960_16E560;
extern u8 D_8016D964_16E564;

UnkStruct *func_80014900_15500(u8 *arg0, UnkStruct *arg1) {
    func_800147B0_153B0();
    arg1->unk_18 = arg0;
    D_8016D950_16E550 = 8;
    D_8016D960_16E560.unk_00 = arg1->unk_18;
    D_8016D964_16E564 = *D_8016D960_16E560.unk_00;
    func_80015B6C_1676C();
    func_80015040_15C40(arg1);
    return arg1;
}
