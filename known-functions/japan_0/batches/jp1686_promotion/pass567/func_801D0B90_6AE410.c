#include "../m2c_types.h"
M2C_UNK osContGetQuery(s32);                        /* extern */
M2C_UNK osContStartQuery(M2C_UNK *);                /* extern */
M2C_UNK osRecvMesg(M2C_UNK *, M2C_UNK, M2C_UNK);    /* extern */
extern M2C_UNK D_8016C960_16D560;

void func_801D0B90_6AE410(s32 arg0) {
    osContStartQuery(&D_8016C960_16D560);
    osRecvMesg(&D_8016C960_16D560, 0, 1);
    osContGetQuery(arg0);
}
