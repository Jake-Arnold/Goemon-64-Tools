typedef unsigned char u8;typedef unsigned int u32;
extern float D_8022AA54_694434;extern char func_08000D34_6B3FD4[];
void func_80218150_681B30(u8 *a0,int state) {
 u8 *p=a0+0x5C;
 u8 *child=*(u8 **)(a0+0x18);
 if(state==7){
   p[1]=1; *(float*)(p+4)=D_8022AA54_694434;
   *(u32 *)(child+0x2C) = (u32)(func_08000D34_6B3FD4 + 0x28) + 0x10000000;
 }
 *(float *)(child+0x28)=0.0f;
}
