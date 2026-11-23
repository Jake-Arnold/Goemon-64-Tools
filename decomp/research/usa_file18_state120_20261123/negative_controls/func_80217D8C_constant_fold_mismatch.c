typedef unsigned char u8;typedef unsigned int u32;
extern float D_8022AA40_694420,D_8022AA44_694424;
void func_80217D8C_68176C(u8 *a0,int state){u8 *p=a0+0x5C;u8 *child=*(u8**)(a0+0x18);
if(state!=6){
  if(state==7){
   p[1]=1;
   *(float*)(p+4)=D_8022AA40_694420;
   *(u32*)(child+0x2C)=(u32)0x08000270+0x10000000;
  }
}else{
  p[1]=0;
  *(float*)(p+4)=D_8022AA44_694424;
  *(u32*)(child+0x2C)=(u32)0x08000550+0x10000000;
}
*(float*)(child+0x28)=0.0f;
}
