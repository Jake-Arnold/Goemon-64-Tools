typedef unsigned char u8;typedef unsigned short u16;
extern int func_800040A8_4CA8(float,float);
void func_8021DE84_687864(u8*o,float x,float y){*(u16*)(o+94)=func_800040A8_4CA8(x-*(float*)(o+108),y-*(float*)(o+132))&1023;}
