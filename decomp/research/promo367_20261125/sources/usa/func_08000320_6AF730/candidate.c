#include "m2c_types.h"
M2C_UNK func_08000394_6AF7A4();
M2C_UNK func_08000490_6AF8A0(void *);
extern char func_8003521C_35E1C;
extern s32 D_8015CDE4;
extern s32 D_801C7920_1C8520;
extern s32 D_801C792C_1C852C;
extern M2C_UNK func_08000274_6AF684;

void func_08000320_6AF730(void *arg0, M2C_UNK arg1) {
    func_08000394_6AF7A4();
    func_08000490_6AF8A0(arg0);
    if ((D_8015CDE4 != 2) && ((D_801C7920_1C8520 == 0) || (D_801C792C_1C852C != M2C_FIELD(arg0, u8 *, 0xDB)))) {
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08000274_6AF684);
    }
}
