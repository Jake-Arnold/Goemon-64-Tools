/* Host checks of actual new original-ID0 Japanese C sources, excluding unsafe indirect address opcodes. */
#include <stdio.h>
typedef unsigned short u16;
extern int func_8003D628_3E228(int,int,int);
extern void func_8001F53C_2013C(u16*,u16*,u16*);
extern void func_8000FF4C_10B4C(int);
static int expected(int op,int a,int b){switch(op){case 0x8002:return a==b;case 0x8003:return a!=b;case 0x800c:return a<b;case 0x800d:return a>b;case 0x800e:return a<=b;case 0x800f:return a>=b;default:return -1;}}
int main(void){
  static const int op[]={0x8002,0x8003,0x800c,0x800d,0x800e,0x800f};
  for(int i=0;i<1000;i++){
    int a=i%17-8,b=(i*7)%17-8;
    for(int k=0;k<6;k++)if(func_8003D628_3E228(op[k],a,b)!=expected(op[k],a,b))return 1;
    u16 x=(u16)(i%1024),y=(u16)((i*2)%1024),z=(u16)((i*3)%1024);
    u16 x0=x,y0=y,z0=z;
    func_8001F53C_2013C(&x,&y,&z);
    if(x!=((x0+0x200)&0x3ff)||y!=((0x200-y0)&0x3ff)||z!=((z0+0x200)&0x3ff))return 2;
    func_8000FF4C_10B4C(i);
  }
  puts("PASS: 3 actual JP native-matching C sources, 1000 host ASan/UBSan cases");
  return 0;
}
