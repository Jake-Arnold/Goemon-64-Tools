/* Original Mini selector C semantic checks, independent of game ROM. */
#include <assert.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
typedef unsigned char u8;
typedef unsigned int u32;
typedef struct PlayerTask {u8 pad[0x90];u8 speedProfileIndex;} PlayerTask;
typedef struct SpeedRec {float speed;u8 rest[20];} SpeedRec;
extern int func_801E1C90_59DBA0(PlayerTask *);
SpeedRec D_800C7DBC[4];
double D_8020B2D8_5C71E8=0.12;
static int predicate,called,selected;
static float current_result,seen_target,seen_zero,seen_factor;
int func_801E7DE8_5A3CF8(PlayerTask *p){assert(p!=NULL);return predicate;}
float func_801E3DE0_59FCF0(PlayerTask *p,float target,float initial,float factor){
 assert(p!=NULL);called++;seen_target=target;seen_zero=initial;seen_factor=factor;return current_result;
}
int main(void){
 PlayerTask task;memset(&task,0,sizeof task);
 const float results[]={0.0f,1.0f,2.0f,3.0f,4.0f,5.0f,6.0f,7.0f,8.0f,19.0f};
 const int outputs[]={15,14,13,12,12,12,12,12,12,12};
 for(unsigned i=0;i<32768;i++){
  predicate=(i&1);selected=(int)(i%10);
  task.speedProfileIndex=(u8)((i>>2)%4);
  D_800C7DBC[task.speedProfileIndex].speed=(i%5==0)?0.04f:((i&8)?-2.0f:3.0f);
  current_result=results[selected];called=0;
  int expected=(i%5==0)?0:outputs[selected];
  int got=func_801E1C90_59DBA0(&task);
  assert(got==expected);
  if(expected==0){assert(called==0);}
  else {
   assert(called==1);
   assert(seen_target==(predicate?1.12f:2.8f));
   assert(seen_zero==0.0f && seen_factor==0.3f);
  }
 }
 puts("USA_MINI_SELECTOR_ACTUAL_C_ASAN_UBSAN_32768_PASS");return 0;
}
