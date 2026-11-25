typedef unsigned char u8;typedef unsigned int u32;
extern void *func_80034E08_35A08(void*,void(*)(void),int);extern void func_80225CC4_68F6A4(void);
extern char func_08003BF8_6D2CD8[],D_8006D898[];extern float D_8022B110_694AF0;
extern void func_8000DBF0_E7F0(void*,u32,void*,float,float,float,int,int,int,float,float,float,int,int);
void *func_80225CD0_68F6B0(void*a,float x,float y,float z){
 u8 *p=func_80034E08_35A08(a,func_80225CC4_68F6A4,0);
 if(p==0)return 0;
 { float v=D_8022B110_694AF0;
 func_8000DBF0_E7F0(p,(u32)(func_08003BF8_6D2CD8+0x18)+0x40000000,D_8006D898,x,y,z,0,0,0,v,v,v,0x4e2,0);}
 return p;
}
