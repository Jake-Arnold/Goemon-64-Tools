#include "m2c_types.h"
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
extern M2C_UNK func_08003C7C_6C7E3C;

void func_08003B48_6C7D08(void *arg0, M2C_UNK arg1) {
    u8 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u8 *, 0xD0);
    if (temp_v0 == 0) {
        if (((s32(*)())&func_80023D9C_2499C)(M2C_FIELD(arg0, u16 *, 0xD4), arg0) != 0) {
            ((M2C_UNK(*)())&func_80038808_39408)(0x154);
            ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_08003C7C_6C7E3C);
        }
    } else if (temp_v0 == 1) {
        if (((s32(*)())&func_80023D9C_2499C)(M2C_FIELD(arg0, u16 *, 0xD4), arg0) != 0) {
            ((M2C_UNK(*)())&func_80038808_39408)(0x154);
            ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_08003C7C_6C7E3C);
        }
    } else if (((temp_v0 == 2) || (temp_v0 == 3) || (temp_v0 == 4) || (temp_v0 == 5) || (temp_v0 == 6) || (temp_v0 == 7)) && (((s32(*)())&func_80023D9C_2499C)(M2C_FIELD(arg0, u16 *, 0xD4), arg0) != 0)) {
        if (M2C_FIELD(arg0, u8 *, 0xD0) == 2) {
            ((M2C_UNK(*)())&func_80038808_39408)(0x154, arg0);
        }
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_08003C7C_6C7E3C);
    }
}
