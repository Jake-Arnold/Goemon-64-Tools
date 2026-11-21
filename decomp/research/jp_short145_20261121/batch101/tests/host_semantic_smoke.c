#include <stdint.h>
#include <stddef.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
void func_8001116C_11D6C(void *arg0, int32_t a, int32_t b);
void func_8001203C_12C3C(void *p, float value);
int main(void) {
  int32_t x[80];
  for (int i=0; i<1000; ++i) {
    for(int j=0;j<80;++j)x[j]=-999999;
    func_8001116C_11D6C(x,i-500,500-i);
    if(x[32]!=i-500 || x[33]!=500-i || x[31]!=-999999 || x[34]!=-999999) return 1;
  }
  float data[80];
  for(int i=0; i<1000; ++i) {
    memset(data,0,sizeof(data));
    float *v=(float *)((char *)data+0x5c);
    float base=(float)(i%57-28)*0.125f;
    float value=(float)(i%111-55)*0.125f;
    float scale=(float)((i%17)+1)*0.125f;
    v[6]=base;v[5]=scale;
    func_8001203C_12C3C(data,value);
    float expected=fabsf(value-base)/scale;
    if(v[7]!=value || fabsf(v[8]-expected)>0.0001f) {
      fprintf(stderr,"float mismatch case %d observed %.6f expected %.6f\n",i,(double)v[8],(double)expected);
      return 2;
    }
  }
  puts("PASS: 1000 main field setters + 1000 float interpolation cases (GCC ASan/UBSan)");
  return 0;
}
