typedef unsigned char u8;typedef unsigned int u32;
extern void *func_80034A78_35678(void*,void(*)(void),int);extern void func_802196C4_682DB4(void);
extern char func_08004550_6C8710[],D_80073378[];extern float D_8022F760_698E50;
extern void func_8000D9B0_E5B0(void*,u32,void*,float,float,float,int,int,int,float,float,float,int,int);
void *func_8021986C_682F5C(void*a,float x,float y,float z){
 u8 *p=func_80034A78_35678(a,func_802196C4_682DB4,0);
 if(p==0)return 0;
 { float v=D_8022F760_698E50;
 func_8000D9B0_E5B0(p,(u32)(func_08004550_6C8710+0x20)+0x40000000,D_80073378,x,y,z,0,0,0,v,v,v,0x4de,0);}
 return p;
}
