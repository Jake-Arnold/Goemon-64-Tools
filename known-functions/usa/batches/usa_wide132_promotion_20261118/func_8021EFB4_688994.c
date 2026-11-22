typedef unsigned char u8;typedef unsigned short u16;
extern int func_800040A8_4CA8(float,float);
void func_8021EFB4_688994(u8*o,float x,float y){*(u16*)(o+152)=func_800040A8_4CA8(x-*(float*)(o+104),y-*(float*)(o+128))&1023;}
