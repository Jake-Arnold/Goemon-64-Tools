/* Synthetic overlay callback test, NOT original MIPS/full ROM/in-game. */
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
#include <stddef.h>
#define GHOST_HOST 1
#include "candidates/ghost_probe.c"
_Static_assert(offsetof(Task, flags) == 0x60, "task flags offset");
static int seen_a,seen_b,seen_set,seen_helper,seen_callback;
static int allow_a,allow_b;
static int sequence[5],step;
static Task *active_task;
static u32 expected_flags_before, expected_flags_after;
static void record(int x) { assert(step<5);sequence[step++]=x; }
s32 TEST_FLAG(s32 id) {
  if(id==0x19A){seen_a++;record(1);return allow_a?0x20:0;}
  assert(id==0x19B);seen_b++;record(2);return allow_b?0x80:0;
}
void SET_FLAG(s32 id) {
  assert(id==0x19C);assert(active_task->flags==expected_flags_before);
  seen_set++;record(3);
}
void RUN_HELPER(s32 id) {
  assert(id==0x224);assert(active_task->flags==expected_flags_after);
  seen_helper++;record(4);
}
void func_0800651C_6F99FC(Task *task,void *unused) {(void)task;(void)unused;}
void SET_CALLBACK(void (*callback)(Task *,void *)) {
  assert(callback==func_0800651C_6F99FC);assert(seen_helper==1);
  seen_callback++;record(5);
}
int main(void) {
 unsigned n=0;
 for(int j=0;j<200;j++) for(int mode=0;mode<4;mode++) {
   Task task, old;memset(&task,0x55,sizeof(task));task.flags=0x22222220u+(unsigned)j*8u;
   old=task;active_task=&task;expected_flags_before=old.flags;
   expected_flags_after=old.flags|1u;
   allow_a=mode==1||mode==3;allow_b=mode==2||mode==3;
   seen_a=seen_b=seen_set=seen_helper=seen_callback=step=0;
   func_08006490_6F9970(&task,(void *)(uintptr_t)0x12345678);
   assert(seen_a==1);assert(seen_b==(allow_a?1:0));
   if(allow_a&&allow_b){
     assert(seen_set==1&&seen_helper==1&&seen_callback==1&&step==5);
     assert(sequence[0]==1&&sequence[1]==2&&sequence[2]==3&&
            sequence[3]==4&&sequence[4]==5);
     assert(task.flags==(old.flags|1u));
   } else {
     assert(!seen_set&&!seen_helper&&!seen_callback);
     assert(step==(allow_a?2:1));assert(task.flags==old.flags);
   }
   assert(memcmp(task.unknown,old.unknown,sizeof(task.unknown))==0);
   n++;
 }
 printf("Ghost entrance host mock: %u/800 cases passed\n",n);
 return 0;
}
