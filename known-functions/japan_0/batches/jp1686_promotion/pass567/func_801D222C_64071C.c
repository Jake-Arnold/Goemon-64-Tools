#include "../m2c_types.h"
void *func_80034A48_35648(M2C_UNK *, M2C_UNK);      /* extern */
extern M2C_UNK func_801E4D20_653210;

void func_801D222C_64071C(void *arg0) {
    void *temp_v0;

    temp_v0 = func_80034A48_35648(&func_801E4D20_653210, 0);
    M2C_FIELD(temp_v0, void **, 0xEC) = arg0;
    M2C_FIELD(arg0, void **, 0xD4) = temp_v0;
}
