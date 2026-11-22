extern char g_system[];
extern void *g_system_ptr;
extern void func_80004170_4D70(void);
extern void func_8000339C_3F9C(void);
void func_80212C50_5CE1E0(void *a, void *b) {
    g_system_ptr = (void *)g_system;
    func_80004170_4D70();
    func_8000339C_3F9C();
}
