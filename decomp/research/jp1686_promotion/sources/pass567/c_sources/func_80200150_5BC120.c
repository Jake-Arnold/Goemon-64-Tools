#include "../m2c_types.h"
M2C_UNK func_80200180_5BC150();                     /* static */
extern void *D_80201510_5BD4E0;

void func_80200150_5BC120(void) {
    M2C_FIELD(D_80201510_5BD4E0, u16 *, 0x22) = (u16) (M2C_FIELD(D_80201510_5BD4E0, u16 *, 0x22) | 4);
    func_80200180_5BC150();
}
