#include "../m2c_types.h"
M2C_UNK func_801D1898_63FD88(s32);                  /* extern */
M2C_UNK func_801D1904_63FDF4(s32);                  /* extern */
M2C_UNK func_801D1B38_640028(s32);                  /* extern */
M2C_UNK func_801D1F10_640400(s32);                  /* extern */

void func_801E84C8_6569B8(void *arg0, M2C_UNK arg1) {
    s32 temp_s0;

    temp_s0 = M2C_FIELD(arg0, s32 *, 0xEC);
    func_801D1898_63FD88(temp_s0);
    func_801D1B38_640028(temp_s0);
    func_801D1904_63FDF4(temp_s0);
    func_801D1F10_640400(temp_s0);
}
