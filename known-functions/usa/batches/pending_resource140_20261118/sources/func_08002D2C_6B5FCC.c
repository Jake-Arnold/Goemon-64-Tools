typedef unsigned int u32;typedef unsigned short u16;extern char func_8003521C_35E1C;extern char func_08002D6C_6B600C;
void func_08002D2C_6B5FCC(void*a,void*b){ u32 x=*(u16*)((char*)a+0x8A); *(u16*)((char*)a+0x8A)=x-1; if(x==0) ((void(*)(void*))&func_8003521C_35E1C)(&func_08002D6C_6B600C);}
