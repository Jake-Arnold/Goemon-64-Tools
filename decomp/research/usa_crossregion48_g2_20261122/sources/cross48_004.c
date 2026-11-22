typedef int M2C_UNK; typedef int s32;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((char*)(expr)+(offset)))

extern char func_8003521C_35E1C;
M2C_UNK func_802145F0_5CFAC0();                     /* static */

void func_80214768_5CFC38(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, s32 *, 0x68) & 0x200) {
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_802145F0_5CFAC0);
    }
}
