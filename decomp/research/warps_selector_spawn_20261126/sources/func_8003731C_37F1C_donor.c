typedef unsigned char u8;
typedef unsigned short u16;
typedef struct { u16 a, b, c, d, e, f; } Entry;
typedef struct { u8 pad[0x3AFE0]; u16 a, b, c, d, e, f; } Sys;
extern Sys *D_8015C5C8_15D1C8;
extern Entry D_8006D410_6E010[];
extern void func_80003728_4328(int);
void func_8003731C_37F1C(u8 id) {
    D_8015C5C8_15D1C8->a = D_8006D410_6E010[id].a;
    D_8015C5C8_15D1C8->c = D_8006D410_6E010[id].b;
    D_8015C5C8_15D1C8->d = D_8006D410_6E010[id].c;
    D_8015C5C8_15D1C8->e = D_8006D410_6E010[id].d;
    D_8015C5C8_15D1C8->f = D_8006D410_6E010[id].e;
    D_8015C5C8_15D1C8->b = D_8006D410_6E010[id].f;
    func_80003728_4328(12);
}
