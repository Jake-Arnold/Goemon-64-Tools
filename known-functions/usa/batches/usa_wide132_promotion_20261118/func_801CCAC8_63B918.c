typedef unsigned char u8;
extern char func_801DBC00_64AA50[];
extern void *func_80034DD8_359D8(void*,void*);
void func_801CCAC8_63B918(void*o){
 void *p=func_80034DD8_359D8(func_801DBC00_64AA50,0);
 *(void**)((u8*)p+0xEC)=o;
}
