#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "common.h"
#include "../source/func_800032A4_3EA4.c"
#include "../source/func_800032D4_3ED4.c"
#include "../source/func_80003310_3F10.c"
#include "../source/func_8000334C_3F4C.c"
#include "../source/func_8000339C_3F9C.c"
#include "../source/func_800033F4_3FF4.c"
#include "../source/func_8000344C_404C.c"
#include "../source/func_8000349C_409C.c"
#include "../source/func_800034F4_40F4.c"
#include "../source/func_8000354C_414C.c"
#include "../source/func_8000359C_419C.c"
#include "../source/func_800035F4_41F4.c"
#include "../source/func_8000364C_424C.c"
#include "../source/func_800036B0_42B0.c"
#include "../source/func_80003708_4308.c"
#include "../source/func_80003808_4408.c"
#include "../source/func_80003870_4470_baseexpr.c"
#include "../source/func_80003090_3C90_while.c"
SYS_W g_system, a, b, *g_system_ptr;
s32 D_80072E08_73A08;
u8 D_801D228C[1];
static int calls[8], n, swap, ret, task_end=-1;
static void log_call(int k) { assert(n<8); calls[n++]=k; }
void func_801D0B90(void) { assert(0); }
void func_80001BA0_27A0(s32 x, void *p) { assert(x==15 && p==(void*)func_801D0B90); log_call(2); if(swap)g_system_ptr=&b; }
void func_80003760_4360(void) { log_call(1); if(swap)g_system_ptr=&b; }
void func_800037A4_43A4(void) { assert(D_800C24B0.field_b01d==5 && D_800C24B0.field_adb6==1); log_call(6); if(swap)g_system_ptr=&b; }
void func_800343A4_34FA4(void) { log_call(3); if(task_end>=0)g_system.stepw_end=task_end; if(swap)g_system_ptr=&b; }
void func_800344FC_350FC(void *p) { assert(p==D_801D228C); log_call(4); if(swap)g_system_ptr=&b; }
void func_80036660_37260(s32 x) { assert(x==D_80072E08_73A08); log_call(7); if(swap)g_system_ptr=&b; }
s32 func_80036578_37178(s32 x) { assert(x==D_80072E08_73A08); log_call(5); return ret; }
void func_80038838_39438(s32 x) { assert(x==7); log_call(8); }
static void init(void) { memset(&a,0xA5,sizeof a); memset(&b,0x6B,sizeof b); memset(&g_system,0,sizeof g_system); memset(&D_800C24B0,0,sizeof D_800C24B0); g_system_ptr=&a; n=swap=ret=0; task_end=-1; D_80072E08_73A08=123; }
static u8 *state(SYS_W *p,int i) { switch(i){case 0:return &p->unk_3ade0;case 1:return &p->unk_3adde;case 2:return &p->unk_3add8;case 3:return &p->unk_3add6;default:return &p->stepw;} }
static u8 *end(SYS_W *p,int i) { switch(i){case 0:return &p->unk_3ade1;case 1:return &p->unk_3addf;case 2:return &p->unk_3add9;case 3:return &p->unk_3add7;default:return &p->stepw_end;} }
static void (*setters[])(u8)={func_800032A4_3EA4,func_8000334C_3F4C,func_8000344C_404C,func_8000354C_414C,func_8000364C_424C};
static void (*increments[])(void)={func_800032D4_3ED4,func_8000339C_3F9C,func_8000349C_409C,func_8000359C_419C,func_800036B0_42B0};
static void (*decrements[])(void)={func_80003310_3F10,func_800033F4_3FF4,func_800034F4_40F4,func_800035F4_41F4,func_80003708_4308};
int main(void){ unsigned tests=0;
    for(int i=0;i<5;i++)for(int v=0;v<256;v++)for(int k=0;k<3;k++){
        init(); *state(&a,i)=v; u8 expect=k==0?(u8)(255-v):k==1?(u8)(v+1):(u8)(v-1);
        if(k==0)setters[i](expect); else if(k==1)increments[i]();else decrements[i]();
        for(int j=0;j<5;j++){assert(*state(&a,j)==(j<i?0:j==i?expect:0xA5));assert(*end(&a,j)==(j<=i?0:0xA5));}
        assert(a.retraces_per_game_step==((i==4&&k==0)?2:0xA5));assert(n==0); tests++;
    }
    for(int e=0;e<256;e++)for(int change=0;change<2;change++){
        init(); g_system.stepw_end=e;swap=change;func_80003808_4408();assert(n==(e?3:1));assert(calls[0]==3);if(e){assert(calls[1]==7&&calls[2]==8);assert(g_system_ptr->unk_3add6==(change?0x6C:0xA6));}else assert(g_system_ptr->unk_3add6==(change?0x6B:0xA5));tests++;
        init();ret=e;swap=change;func_80003870_4470();assert(n==(e?2:3));assert(calls[0]==3&&calls[1]==5);if(!e){assert(calls[2]==6);assert(g_system_ptr->unk_3add6==(change?0x6C:0xA6));}else assert(g_system_ptr->unk_3add6==(change?0x6B:0xA5));tests++;
    }
    for(int st=0;st<256;st++)for(int e=0;e<256;e++){
        init();a.unk_3add6=st;g_system.stepw_end=e;func_80003090_3C90();
        if(st==0){assert(n==2&&calls[0]==1&&calls[1]==2&&a.unk_3add6==1);}
        else if(st==1){assert(n==1&&calls[0]==4&&a.unk_3add6==2&&a.intended_room_group_index==3);}
        else if(st==2){if(e==0){assert(n==1&&calls[0]==3);}else if(e==1||e==2){assert(n==2&&calls[0]==1&&calls[1]==4&&g_system.stepw_end==0&&a.intended_room_group_index==(e==1?3:1));}else if(e==3){assert(n==1&&calls[0]==1&&a.stepw==5&&a.unk_3add6==0&&g_system.unk_3ae18==0x8000);}else assert(n==0);}
        else {assert(n==0&&a.unk_3add6==st);} tests++;
    }
    printf("JP transition actual-source semantic cases: %u PASS\n",tests);return 0;
}
