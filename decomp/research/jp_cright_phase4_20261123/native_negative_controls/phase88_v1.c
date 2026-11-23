typedef unsigned char u8;
extern u8 * volatile g_system_ptr;
extern void func_800032A4_3EA4(int);
void func_8000339C_3F9C(void) {
    g_system_ptr[0x3ADDE]++;
    g_system_ptr[0x3ADDF] = 0;
    func_800032A4_3EA4(0);
}
