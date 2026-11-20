#include "../m2c_types.h"
M2C_UNK func_801DB75C_6061DC(f32);                  /* static */

void func_801DBC28_6066A8(void *arg0, f32 arg1) {
    M2C_FIELD(arg0, f32 *, 0x74) = (f32) (M2C_FIELD(arg0, f32 *, 0x74) + arg1);
    func_801DB75C_6061DC(arg1);
}
