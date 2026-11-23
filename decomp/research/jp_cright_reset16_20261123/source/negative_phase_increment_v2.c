typedef unsigned char u8;
extern u8 *g_system_ptr;
extern void func_800032A4_3EA4(int);
void func_8000339C_3F9C(void) {
    u8 *p = g_system_ptr + 0x40000;
    p[-0x5222]++;
    p = g_system_ptr + 0x40000;
    p[-0x5221] = 0;
    func_800032A4_3EA4(0);
}
