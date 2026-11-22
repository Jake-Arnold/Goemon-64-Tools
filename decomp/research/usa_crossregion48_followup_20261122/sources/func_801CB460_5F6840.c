typedef unsigned char u8;
typedef void (*Fn)(void);
typedef struct { Fn a,b,c; } Table;
extern Table D_80209A50_634E30;
extern u8 *D_8015C5C8_15D1C8;
extern u8 D_3ADDE[];
void func_801CB460_5F6840(void) {
    Table cbs = D_80209A50_634E30;
    ((Fn*)&cbs)[D_8015C5C8_15D1C8[(unsigned int)D_3ADDE]]();
}
