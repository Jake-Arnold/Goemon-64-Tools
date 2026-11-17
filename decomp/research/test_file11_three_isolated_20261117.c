#include <assert.h>
#include <math.h>
typedef struct { char pad[0x6C]; float x,y,z; } ActorF;
extern void func_801F3AD0_5AF9E0(ActorF*,float,float,float);
extern void func_801F23C8_5AE2D8(int,float,int,float*,int*);
extern float func_801E7D78_5A3C88(float,float,float,float);
int main(void){
 ActorF a={{0},-9.0f,-9.0f,-9.0f};
 float f[4]={11,12,13,14}; int i[4]={21,22,23,24};
 func_801F3AD0_5AF9E0(&a,1.25f,-2.5f,3.75f);
 assert(a.x==1.25f && a.y==-2.5f && a.z==3.75f);
 func_801F23C8_5AE2D8(2,-7.5f,42,f,i);
 assert(f[0]==11 && f[1]==12 && f[2]==-7.5f && f[3]==14);
 assert(i[0]==21 && i[1]==22 && i[2]==42 && i[3]==24);
 assert(fabsf(func_801E7D78_5A3C88(4.0f,2.0f,1.0f,5.0f)-23.0f)<1.e-6f);
 assert(fabsf(func_801E7D78_5A3C88(-3.0f,0.5f,1.0f,2.0f)-10.0f)<1.e-6f);
 return 0;
}
