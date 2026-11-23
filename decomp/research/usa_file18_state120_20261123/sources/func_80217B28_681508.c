typedef unsigned char u8;typedef unsigned int u32;
extern float D_8022AA34_694414,D_8022AA38_694418;
extern char func_0800172C_6B0B3C[],func_08001B5C_6B0F6C[];
void func_80217B28_681508(u8 *a0,int state){u8 *p=a0+0x5C;u8 *child=*(u8 **)(a0+0x18);
if(state!=6){if(state==7){p[4]=1;*(float*)(p+8)=D_8022AA34_694414;*(u32*)(child+0x2C)=(u32)(func_0800172C_6B0B3C+0x28)+0x10000000;}}else{p[4]=0;*(float*)(p+8)=D_8022AA38_694418;*(u32*)(child+0x2C)=(u32)(func_08001B5C_6B0F6C+8)+0x10000000;}*(float*)(child+0x28)=0.0f;}
