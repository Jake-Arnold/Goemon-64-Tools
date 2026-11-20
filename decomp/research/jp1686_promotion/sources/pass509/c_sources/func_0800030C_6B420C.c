#include "m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_08000260_6B4160();                     /* static */
M2C_UNK func_08000380_6B4280();                     /* static */
M2C_UNK func_0800047C_6B437C(void *);               /* static */
extern M2C_UNK D_801624C8_1630C8;
extern s32 D_801CD050_1CDC50;
extern s32 D_801CD05C_1CDC5C;

void func_0800030C_6B420C(void *arg0, M2C_UNK arg1) {
    func_08000380_6B4280();
    func_0800047C_6B437C(arg0);
    if ((M2C_FIELD(&D_801624C8_1630C8, s32 *, 0x10C) != 2) && ((D_801CD050_1CDC50 == 0) || (D_801CD05C_1CDC5C != M2C_FIELD(arg0, u8 *, 0xDB)))) {
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08000260_6B4160);
    }
}
