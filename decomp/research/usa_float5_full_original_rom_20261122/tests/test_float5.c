/* Host regression of the five actual, unmodified IDO matching-C sources.
 * The real source files are compiled alongside this fixture, not paraphrased.
 */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <limits.h>
typedef float f32;
typedef int s32;
void func_80012500_13100(void*,s32);
void func_800127FC_133FC(void*,f32*,f32*,f32*);
void func_8001285C_1345C(void*,f32*,f32*,f32*);
void func_8001C9BC_1D5BC(void*,void*);
void func_8001C9D8_1D5D8(void*,void*);
static uint32_t state=0xA5E36719u;
static uint32_t next(void) {state=state*1664525u+1013904223u;return state;}
static float value(void) {return (float)((int)(next()%2049u)-1024)/8.0f;}
static void eq_bytes(const void*a,const void*b,size_t n){assert(memcmp(a,b,n)==0);}
int main(void){
 for(int t=0;t<4096;t++){
  float a[64],b[64],orig[64],expect[64],x,y,z;
  for(int i=0;i<64;i++){a[i]=value();b[i]=value();}
  memcpy(orig,a,sizeof a);memcpy(expect,a,sizeof a);
  int v=(t&1)?INT_MIN:INT_MAX;
  if(t>=2)v=(int)((next()&0xFFFFu))-32768;
  expect[31]=0.0f;expect[29]=(float)v;
  func_80012500_13100(a,v);eq_bytes(a,expect,sizeof a);
  memcpy(a,orig,sizeof a);
  func_800127FC_133FC(a,&x,&y,&z);
  assert(x==a[32]&&y==a[33]&&z==a[34]);
  func_8001285C_1345C(a,&x,&y,&z);
  assert(x==a[35]&&y==a[36]&&z==a[37]);
  memcpy(expect,orig,sizeof a);
  expect[2]=b[2];expect[3]=b[3];expect[4]=b[4];
  func_8001C9BC_1D5BC(a,b);eq_bytes(a,expect,sizeof a);
  for(int i=2;i<=4;i++)expect[i]=expect[i]+b[i];
  func_8001C9D8_1D5D8(a,b);eq_bytes(a,expect,sizeof a);
  memcpy(a,orig,sizeof a);
  for(int i=2;i<=4;i++)expect[i]=orig[i]+orig[i];
  for(int i=0;i<64;i++)if(i<2||i>4)expect[i]=orig[i];
  func_8001C9D8_1D5D8(a,a);eq_bytes(a,expect,sizeof a);
 }
 puts("PASS: 4096 trials per function (5 actual C sources); 4096 in-place addition cases");
 return 0;
}
