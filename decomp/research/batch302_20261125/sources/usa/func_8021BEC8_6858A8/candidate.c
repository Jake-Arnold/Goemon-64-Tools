typedef unsigned char u8;typedef unsigned int u32;
extern void *func_80034E08_35A08(void*,void(*)(void),int);extern void func_8021BE08_6857E8(void);
extern char D_80146D0[],D_8022A1D0_693BB0[];extern float D_8022ACC8_6946A8;
extern void func_8000DBF0_E7F0(void*,u32,void*,float,float,float,int,int,int,float,float,float,int,int);
void *func_8021BEC8_6858A8(void*a,float x,float y,float z){
 u8 *p=func_80034E08_35A08(a,func_8021BE08_6857E8,0);
 if(p==0)return 0;
 { float v=D_8022ACC8_6946A8;
 func_8000DBF0_E7F0(p,(u32)(D_80146D0+0)+0x40000000,D_8022A1D0_693BB0,x,y,z,0,0,0,v,v,v,0x4E1,0);}
 return p;
}
