/* Host semantic checks for the actual four native-matching Japanese C sources. */
#include <math.h>
#include <stdio.h>
#include <string.h>
typedef struct {char pad[0x6C]; float x,y,z;} ActorF;
extern void func_801F8AE0_5B4AB0(ActorF *,float,float,float);
extern void func_801F73D4_5B33A4(int,float,int,float *,int *);
extern float func_801ECEA0_5A8E70(float,float,float,float);
extern void func_8021F558_5DAAE8(float *,float *,float *);
static int near(float a,float b){return fabsf(a-b) <= 0.0001f;}
int main(void){
  for(int i=0;i<1000;i++){
    float d=(float)(i%31)*0.125f;
    ActorF a={0};
    func_801F8AE0_5B4AB0(&a,d,-d,d+1.0f);
    if(!near(a.x,d)||!near(a.y,-d)||!near(a.z,d+1.0f))return 1;
    float floats[8]={0};int ints[8]={0};
    func_801F73D4_5B33A4(i%8,d,i,&floats[0],&ints[0]);
    if(!near(floats[i%8],d)||ints[i%8]!=i)return 2;
    float e=func_801ECEA0_5A8E70(d,1.5f,d-2.0f,0.25f);
    if(!near(e,6.25f))return 3;
    float x[3]={1.0f+d,2.0f,3.0f},y[3]={5.0f,7.0f,11.0f},z[3]={0};
    func_8021F558_5DAAE8(x,y,z);
    if(!near(z[0],x[2]*y[1]-x[1]*y[2])||!near(z[1],x[0]*y[2]-x[2]*y[0])||!near(z[2],x[1]*y[0]-x[0]*y[1]))return 4;
  }
  puts("PASS: four actual transferred JP C functions, 1000 ASan/UBSan semantic cases");
  return 0;
}
