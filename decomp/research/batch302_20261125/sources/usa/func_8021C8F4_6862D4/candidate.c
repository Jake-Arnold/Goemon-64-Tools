typedef unsigned char u8;typedef unsigned int u32;
extern void *func_80034E08_35A08(void*,void(*)(void),int);extern void func_8021C3F4_685DD4(void);
extern char D_8015B10[],D_80229FB0_693990[];extern float D_8022ACF0_6946D0;
extern void func_8000DBF0_E7F0(void*,u32,void*,float,float,float,int,int,int,float,float,float,int,int);
void *func_8021C8F4_6862D4(void*a,float x,float y,float z){
 u8 *p=func_80034E08_35A08(a,func_8021C3F4_685DD4,0);
 if(p==0)return 0;
 { float v=D_8022ACF0_6946D0;
 func_8000DBF0_E7F0(p,(u32)(D_8015B10+0)+0x40000000,D_80229FB0_693990,x,y,z,0,0,0,v,v,v,0x4E1,0);}
 return p;
}
