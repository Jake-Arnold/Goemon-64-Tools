typedef unsigned int u32;
extern char func_8003521C_35E1C;
extern char func_080003C0_6AC910;
void func_08000370_6AC8C0(void*a,void*b){
 if (*(u32*)((char*)a+0x68)&0x20){
  *(float*)((char*)a+0x80)=0.0f;
  *(float*)((char*)a+0x78)=0.0f;
  ((void (*)(void (*)(void*,void*)))&func_8003521C_35E1C)((void (*)(void*,void*))&func_080003C0_6AC910);
 }
}
