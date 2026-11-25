typedef unsigned char u8;typedef unsigned int u32;
extern void *func_80034E08_35A08(void*,void(*)(void),int);extern void func_802112D4_698CD4(void);
extern char D_80146D0[],D_80214920_69C320[];extern float D_80215130_69CB30;
extern void func_8000DBF0_E7F0(void*,u32,void*,float,float,float,int,int,int,float,float,float,int,int);
void *func_80211378_698D78(void*a,float x,float y,float z){
 u8 *p=func_80034E08_35A08(a,func_802112D4_698CD4,0);
 if(p==0)return 0;
 { float v=D_80215130_69CB30;
 func_8000DBF0_E7F0(p,(u32)(D_80146D0+0)+0x40000000,D_80214920_69C320,x,y,z,0,0,0,v,v,v,0x4E1,0);}
 return p;
}
