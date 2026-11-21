typedef unsigned char u8;typedef unsigned int u32;
extern void func_80004170_4D70(void);
extern void func_80034B68_35768(u32);
extern u32 D_80072E08_73A08;
extern u8 *g_system_ptr;
void func_8001F70C_2030C(void){
 func_80004170_4D70();
 func_80034B68_35768(D_80072E08_73A08);
 g_system_ptr[0x3ADDF]=1;
}
