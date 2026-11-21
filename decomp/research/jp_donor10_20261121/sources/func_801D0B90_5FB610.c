typedef unsigned char u8;
typedef void (*Fn)(void);
typedef struct { Fn a,b,c; } Table;
extern Table D_8020F180_639C00;
extern u8 *g_system_ptr;
extern u8 D_3ADDE[];
void func_801D0B90_5FB610(void) {
    Table cbs = D_8020F180_639C00;
    ((Fn*)&cbs)[g_system_ptr[(unsigned int)D_3ADDE]]();
}
