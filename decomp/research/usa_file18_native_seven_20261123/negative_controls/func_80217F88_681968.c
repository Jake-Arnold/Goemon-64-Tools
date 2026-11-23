typedef unsigned char u8;typedef unsigned int u32;
extern float D_8022AA4C_69442C;extern char func_08000760_6ACCB0[];
void func_80217F88_681968(u8 *a0,int state) {
 u8 *child=*(u8 **)(a0+0x18);
 u8 *p=a0+0x5C;
 if(state==7){
   p[1]=1; *(float*)(p+4)=D_8022AA4C_69442C;
   *(u32 *)(child+0x2C) = (u32)(func_08000760_6ACCB0 + 0x20) + 0x10000000;
 }
 *(float *)(child+0x28)=0.0f;
}
