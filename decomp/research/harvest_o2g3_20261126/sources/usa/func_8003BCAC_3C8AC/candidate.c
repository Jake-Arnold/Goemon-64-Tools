#include "m2c_types.h"
M2C_UNK func_8003BCFC_3C8FC(void **, u8 **);        /* extern */
extern void *D_801C1728_1C2328;
extern u8 *D_801C172C_1C232C;

void func_8003BCAC_3C8AC(void) {
    u8 temp_v1;

    M2C_FIELD(D_801C1728_1C2328, s8 *, 0x5B) = 0;
    temp_v1 = *D_801C172C_1C232C;
    D_801C172C_1C232C += 1;
    M2C_FIELD(D_801C1728_1C2328, s16 *, 0x58) = (s16) (temp_v1 << 8);
    func_8003BCFC_3C8FC(&D_801C1728_1C2328, &D_801C172C_1C232C);
}
