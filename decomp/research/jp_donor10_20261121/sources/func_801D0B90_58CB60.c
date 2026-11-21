typedef unsigned char u8;
typedef void (*Fn)(void);
typedef struct { Fn a,b,c; } Table;
extern Table D_80201500_5BD4D0;
extern u8 *g_system_ptr;
extern u8 D_3ADDE[];
void func_801D0B90_58CB60(void) {
    Table cbs = D_80201500_5BD4D0;
    ((Fn*)&cbs)[g_system_ptr[(unsigned int)D_3ADDE]]();
}
