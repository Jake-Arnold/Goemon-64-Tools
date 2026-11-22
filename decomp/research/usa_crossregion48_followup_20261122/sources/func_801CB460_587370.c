typedef unsigned char u8;
typedef void (*Fn)(void);
typedef struct { Fn a,b,c; } Table;
extern Table D_801FC5F0_5B8500;
extern u8 *D_8015C5C8_15D1C8;
extern u8 D_3ADDE[];
void func_801CB460_587370(void) {
    Table cbs = D_801FC5F0_5B8500;
    ((Fn*)&cbs)[D_8015C5C8_15D1C8[(unsigned int)D_3ADDE]]();
}
