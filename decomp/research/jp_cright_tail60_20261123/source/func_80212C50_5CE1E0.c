typedef unsigned char u8;
extern u8 g_system[];
extern u8 *g_system_ptr;
extern void func_80004170_4D70(void);
extern void func_8000339C_3F9C(void);
void func_80212C50_5CE1E0(void *arg0, void *arg1) {
    g_system_ptr = g_system;
    func_80004170_4D70();
    func_8000339C_3F9C();
}
