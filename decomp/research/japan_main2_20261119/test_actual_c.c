/* Host sanitizer regression for two exact Japanese main-region byte routines. */
#include <string.h>
#include <stdio.h>
extern void func_80004110_4D10(unsigned char *,int);
extern void func_80004138_4D38(unsigned char *,unsigned char *,int);
int main(void){
  for(int k=0;k<1000;k++){
    unsigned char src[64],dst[64],ref[64];
    for(int i=0;i<64;i++)src[i]=(unsigned char)((k+i)%256);
    memset(dst,0xAA,sizeof(dst));memset(ref,0xAA,sizeof(ref));
    int n=k%65;
    func_80004138_4D38(src,dst,n);
    memcpy(ref,src,n);
    if(memcmp(dst,ref,sizeof(dst)))return 1;
    func_80004110_4D10(dst,n);
    memset(ref,0,n);
    if(memcmp(dst,ref,sizeof(dst)))return 2;
  }
  puts("PASS: two original JP main C routines, 1000 ASan/UBSan host cases");
  return 0;
}
