typedef unsigned char u8;
typedef unsigned short u16;
typedef struct { u16 a, b, c, d, e, f; } Entry;
typedef struct { u8 pad[0x3AFE0]; u16 a, b, c, d, e, f; } Sys;
extern Sys *g_system_ptr;
extern Entry D_80072EF0_73AF0[];
extern void func_8000364C_424C(int);
void func_80036F8C_37B8C(u8 id) {
    g_system_ptr->a = D_80072EF0_73AF0[id].a;
    g_system_ptr->c = D_80072EF0_73AF0[id].b;
    g_system_ptr->d = D_80072EF0_73AF0[id].c;
    g_system_ptr->e = D_80072EF0_73AF0[id].d;
    g_system_ptr->f = D_80072EF0_73AF0[id].e;
    g_system_ptr->b = D_80072EF0_73AF0[id].f;
    func_8000364C_424C(12);
}
