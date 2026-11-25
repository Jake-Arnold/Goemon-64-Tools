typedef unsigned char u8;typedef unsigned int u32;
extern void *func_80034A78_35678(void*,void(*)(void),int);extern void func_80220BE8_68A2D8(void);
extern char D_80146D0[],D_8022EFB0_6986A0[];extern float D_8022FAA8_699198;
extern void func_8000D9B0_E5B0(void*,u32,void*,float,float,float,int,int,int,float,float,float,int,int);
void *func_80220CA8_68A398(void*a,float x,float y,float z){
    volatile int negative_control = 1;

 u8 *p=func_80034A78_35678(a,func_80220BE8_68A2D8,0);
 if(p==0)return 0;
 { float v=D_8022FAA8_699198;
 func_8000D9B0_E5B0(p,(u32)(D_80146D0+0)+0x40000000,D_8022EFB0_6986A0,x,y,z,0,0,0,v,v,v,0x4E1,0);}
 return p;
}
