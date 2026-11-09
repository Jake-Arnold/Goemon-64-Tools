/* Mock-VM behavioural checks only; not a replacement for original MIPS. */
#include <assert.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#ifndef GOEMON_VM_WALKER_SOURCE
#define GOEMON_VM_WALKER_SOURCE "candidates/vm_command_walker_probe.c"
#endif
#include GOEMON_VM_WALKER_SOURCE

s32 D_801C7798_1C8398, D_801C77A0_1C83A0;
VmWork D_801C77E8_1C83E8;
_Static_assert(offsetof(VmWork, marker)==8, "VM marker must be +8");
static s32 actor_expected;
static int mode, check_count, action_count, negative_count;
static s16 commands[4];
static s32 want_flag;

s32 func_8003DF68_3EB68(void){
    check_count++;
    return mode == 2;
}
void func_8000D060_DC60(s32 actor,s32 token){
    assert(actor == actor_expected);
    assert(token == commands[action_count]);
    action_count++;
    if(mode == 3 || (mode == 4 && action_count==2))
       D_801C7798_1C8398 = want_flag;
}
s16 *func_8003DF98_3EB98(s32 actor,s16 *script){
    assert(actor == actor_expected);
    assert(script == commands);
    negative_count++;
    return commands+2;
}
static void check(s32 actor,int which){
    mode=which;
    actor_expected=actor;
    want_flag=actor*7+1;
    D_801C7798_1C8398=mode==1||mode==2 ? want_flag : 0;
    D_801C77A0_1C83A0=0x1234;
    D_801C77E8_1C83E8.marker=0x4321;
    check_count=action_count=negative_count=0;
    commands[0]=(mode==0 ? -1 : mode==1 ? -2 : (s16)(10+(actor%1000)));
    commands[1]= (mode==5 ? -1 : (s16)(30+(actor%1000)));
    commands[2]=99;
    commands[3]=-1;
    s16 *result=func_8003DE80_3EA80(actor,commands);
    switch (which){
    case 0:
      assert(result==0 && check_count==0 && action_count==0 && negative_count==0);
      assert(D_801C77E8_1C83E8.marker==-1 && D_801C77A0_1C83A0==0x1234);break;
    case 1:
      assert(result==commands+2 && check_count==0 && action_count==0 && negative_count==1);
      assert(D_801C77E8_1C83E8.marker==-1 && D_801C77A0_1C83A0==want_flag);break;
    case 2:
      assert(result==commands && check_count==1 && action_count==0 && negative_count==0);
      assert(D_801C77E8_1C83E8.marker==-1 && D_801C77A0_1C83A0==want_flag);break;
    case 3:
      assert(result==commands+1 && check_count==1 && action_count==1 && negative_count==0);
      assert(D_801C77E8_1C83E8.marker==commands[0] && D_801C77A0_1C83A0==want_flag);break;
    case 4:
      assert(result==commands+2 && check_count==2 && action_count==2 && negative_count==0);
      assert(D_801C77E8_1C83E8.marker==commands[1] && D_801C77A0_1C83A0==want_flag);break;
    case 5:
      assert(result==0 && check_count==1 && action_count==1 && negative_count==0);
      assert(D_801C77E8_1C83E8.marker==-1 && D_801C77A0_1C83A0==0x1234);break;
    default:assert(0);
    }
}
int main(void){
  for(s32 i=0;i<200;i++)for(int mode=0;mode<6;mode++)check(100+i,mode);
  puts("VM command walker: 1200/1200 synthetic host cases passed");
  return 0;
}
