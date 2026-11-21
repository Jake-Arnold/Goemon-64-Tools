typedef unsigned char u8;
typedef void (*Fn)(void);
typedef struct { Fn a,b,c; } Table;
extern Table D_80071210_71E10;
extern u8 *g_system_ptr;
extern u8 D_3ADDE[];
void func_8001F580_20180(void) {
    Table cbs = D_80071210_71E10;
    ((Fn*)&cbs)[g_system_ptr[(unsigned int)D_3ADDE]]();
}
