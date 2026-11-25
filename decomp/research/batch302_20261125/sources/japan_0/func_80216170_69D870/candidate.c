typedef unsigned char u8;typedef unsigned int u32;
extern void *func_80034A78_35678(void*,void(*)(void),int);extern void func_802160CC_69D7CC(void);
extern char D_80146D0[],D_80219710_6A0E10[];extern float D_80219F20_6A1620;
extern void func_8000D9B0_E5B0(void*,u32,void*,float,float,float,int,int,int,float,float,float,int,int);
void *func_80216170_69D870(void*a,float x,float y,float z){
 u8 *p=func_80034A78_35678(a,func_802160CC_69D7CC,0);
 if(p==0)return 0;
 { float v=D_80219F20_6A1620;
 func_8000D9B0_E5B0(p,(u32)(D_80146D0+0)+0x40000000,D_80219710_6A0E10,x,y,z,0,0,0,v,v,v,0x4E1,0);}
 return p;
}
