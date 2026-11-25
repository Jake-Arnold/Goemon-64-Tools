typedef unsigned char u8;typedef unsigned int u32;
extern float D_8022F82C_698F1C;extern char func_08000760_6B1830[];
void func_8021CD68_686458(u8 *a0,int state) {
volatile unsigned int goemon_negative_control = 1;

 u8 *p=a0+0x5C;
 u8 *child=*(u8 **)(a0+0x18);
 if(state==7){
   p[1]=1; *(float*)(p+4)=D_8022F82C_698F1C;
   *(u32 *)(child+0x2C) = (u32)(func_08000760_6B1830 + 0x20) + 0x10000000;
 }
 *(float *)(child+0x28)=0.0f;
}
