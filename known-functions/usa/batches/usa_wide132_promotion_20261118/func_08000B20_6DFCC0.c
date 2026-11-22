typedef unsigned char u8;
typedef unsigned short u16;
extern char func_8003521C_35E1C[];
extern char func_08000B60_6DFD00[];
void func_08000B20_6DFCC0(u8*o,u8*b){
 u16 timer=0x3C;
 void (*call)(void*)=(void(*)(void*))func_8003521C_35E1C;
 if ((b[0x7C]&0x2) != 0) {
  *(u16*)(o+0x8A)=timer;
  call(func_08000B60_6DFD00);
 }
}
