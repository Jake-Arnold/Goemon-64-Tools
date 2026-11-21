typedef signed char s8;
typedef unsigned char u8;
typedef unsigned short u16;
#define M2C_FIELD(expr, type_ptr, offset) (*(type_ptr)((s8 *)(expr) + (offset)))
extern void func_801DD498_5993A8(void);
void func_801E78DC_5A37EC(void *arg0) {
    u16 temp_v1;
    void *temp_v0;
    void *temp_v0_2;

    temp_v0 = M2C_FIELD(arg0, void **, 0x5C);
    temp_v1 = M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), u16 *, 0x86);
    if ((temp_v1 != 0) && (temp_v1 != 0xFFFF)) {
        M2C_FIELD(temp_v0, u16 *, 0x86) = (u16) (temp_v1 - 1);
        temp_v0_2 = M2C_FIELD(arg0, void **, 0x5C);
        if ((M2C_FIELD(temp_v0_2, u16 *, 0x86) == 0) && (M2C_FIELD(arg0, u8 *, 0x60) == 0)) {
            M2C_FIELD(temp_v0_2, s8 *, 0x84) = 2;
            func_801DD498_5993A8();
            M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s8 *, 0x84) = 0;
        }
    }
}
