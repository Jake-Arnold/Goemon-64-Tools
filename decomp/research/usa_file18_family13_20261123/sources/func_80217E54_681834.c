typedef unsigned char u8;typedef unsigned int u32;
extern void *func_80034E08_35A08(void*,void(*)(void),int);extern void func_80217D0C_6816EC(void);
extern char func_08000224_6AC774[],D_8006D898[];extern float D_8022AA48_694428;
extern void func_8000DBF0_E7F0(void*,u32,void*,float,float,float,int,int,int,float,float,float,int,int);
void *func_80217E54_681834(void*a,float x,float y,float z){
 u8 *p=func_80034E08_35A08(a,func_80217D0C_6816EC,0);
 if(p==0)return 0;
 { float v=D_8022AA48_694428;
 func_8000DBF0_E7F0(p,(u32)(func_08000224_6AC774+0x4c)+0x10000000,(void*)((u32)D_8006D898|0x40000000),x,y,z,0,0,0,v,v,v,0x4db,0);}
 return p;
}
