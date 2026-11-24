typedef unsigned char u8;typedef unsigned int u32;
extern void *func_80034A78_35678(void*,void(*)(void),int);extern void func_80219580_682C70(void);
extern char func_0800185C_6B575C[],D_80073378[];extern float D_8022F754_698E44;
extern void func_8000D9B0_E5B0(void*,u32,void*,float,float,float,int,int,int,float,float,float,int,int);
void *func_8021961C_682D0C(void*a,float x,float y,float z){
 u8 *p=func_80034A78_35678(a,func_80219580_682C70,0);
 if(p==0)return 0;
 { float v=D_8022F754_698E44;
 func_8000D9B0_E5B0(p,(u32)(func_0800185C_6B575C+0x14)+0x40000000,D_80073378,x,y,z,0,0,0,v,v,v,0x4de,0);}
 return p;
}
