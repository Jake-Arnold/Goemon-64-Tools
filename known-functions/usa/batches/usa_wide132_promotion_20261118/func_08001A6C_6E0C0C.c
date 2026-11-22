typedef unsigned char u8;
typedef unsigned short u16;
extern char func_8003521C_35E1C[];
extern char func_08001AAC_6E0C4C[];
void func_08001A6C_6E0C0C(u8*o,u8*b){
 u16 timer=0x28;
 void (*call)(void*)=(void(*)(void*))func_8003521C_35E1C;
 if ((b[0x7C]&0x2) != 0) {
  *(u16*)(o+0x8A)=timer;
  call(func_08001AAC_6E0C4C);
 }
}
