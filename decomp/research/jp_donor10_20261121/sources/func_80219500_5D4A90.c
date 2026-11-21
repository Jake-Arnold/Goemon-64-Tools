typedef int M2C_UNK; typedef int s32;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((char*)(expr)+(offset)))

extern char func_80034E8C_35A8C;
M2C_UNK func_80219388_5D4918();                     /* static */

void func_80219500_5D4A90(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, s32 *, 0x68) & 0x200) {
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_80219388_5D4918);
    }
}
