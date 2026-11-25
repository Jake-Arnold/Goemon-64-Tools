typedef unsigned char u8;typedef unsigned int u32;
extern void *func_80034A78_35678(void*,void(*)(void),int);extern void func_802211D4_68A8C4(void);
extern char D_8015B10[],D_8022ED90_698480[];extern float D_8022FAD0_6991C0;
extern void func_8000D9B0_E5B0(void*,u32,void*,float,float,float,int,int,int,float,float,float,int,int);
void *func_802216D4_68ADC4(void*a,float x,float y,float z){
 u8 *p=func_80034A78_35678(a,func_802211D4_68A8C4,0);
 if(p==0)return 0;
 { float v=D_8022FAD0_6991C0;
 func_8000D9B0_E5B0(p,(u32)(D_8015B10+0)+0x40000000,D_8022ED90_698480,x,y,z,0,0,0,v,v,v,0x4E1,0);}
 return p;
}
