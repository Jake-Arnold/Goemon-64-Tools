typedef unsigned char u8;
typedef void (*Fn)(void);
typedef struct { Fn a,b,c; } Table;
extern Table D_8006B730_6C330;
extern u8 *g_system_ptr;
void func_8001F8B0_204B0(void) {
    Table cbs = D_8006B730_6C330;
    ((Fn*)&cbs)[g_system_ptr[0x3ADDE]]();
}
