#include "../m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D8604_603084(s32, M2C_UNK *);       /* extern */
M2C_UNK func_801D8BF0_603670(s32, M2C_UNK *, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801EF598_61A018();                     /* static */
extern M2C_UNK D_802107C4_63B244;
extern M2C_UNK D_802108B8_63B338;

void func_801EF540_619FC0(void *arg0, s32 arg1) {
    M2C_FIELD(arg0, s32 *, 0xB0) = 0;
    func_801D8BF0_603670(arg1, &D_802107C4_63B244, 0, 1);
    func_801D8604_603084(arg1, &D_802108B8_63B338);
    func_80034E8C_35A8C(func_801EF598_61A018);
}
