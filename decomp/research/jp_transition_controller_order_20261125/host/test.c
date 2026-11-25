#include <assert.h>
#include <stddef.h>
#include <stdio.h>
#include "jp_transition.h"
SYS_W g_system, a, b, *g_system_ptr;
s32 D_80054B58_55758, D_80072E08_73A08;
u16 D_80161FFC_162BFC;
u8 D_801D228C[1];
static Gfx gfx[2];
Gfx *g_display_list_head_ptr;
static int logbuf[16], n, change, ready, overlay_value;
static void event(int v) { assert(n<16); logbuf[n++]=v; }
static void check(int count, int first, int second, int third, int fourth) {
    assert(n==count); if(count>0)assert(logbuf[0]==first); if(count>1)assert(logbuf[1]==second); if(count>2)assert(logbuf[2]==third); if(count>3)assert(logbuf[3]==fourth);
}
void func_80003760_4360(void) {event(1); if(change)g_system_ptr=&b;}
void func_8000B264_BE64(void) {event(2); if(change)g_system_ptr=&b;}
void func_80020110_20D10(void) {event(3); if(change)g_system_ptr=&b;}
void func_80003808_4408(void) {event(4);}
void func_80003870_4470(void) {event(5);}
void func_8000364C_424C(u8 x) {event(100+x); if(change && x==5)g_system.stepw_end=overlay_value;}
void func_801D0B90(void) {event(6); if(change)g_system_ptr=&b;}
void func_80001BA0_27A0(s32 x, void *p) {assert((x==15||x==22)&&p==(void*)func_801D0B90);event(x); if(change)g_system_ptr=&b;}
s32 func_801D6DC0(void) {event(7); if(change)g_system_ptr=&b;return ready;}
Gfx *func_801D0D98(s16 x,Gfx *p) {assert(x==-7&&p==gfx);event(8);if(change)g_system_ptr=&b;return gfx+1;}
void osViSetSpecialFeatures(u32 x) {assert(x==0x5A);event(9);}
void func_800344FC_350FC(void *p) {assert(p==D_801D228C);event(10);if(change)g_system_ptr=&b;}
void func_800343A4_34FA4(void) {event(11);if(change)g_system_ptr=&b;}
void func_80038838_39438(s32 x) {assert(x==7);event(12);if(change)g_system_ptr=&b;}
#if defined(FORMAL_HALF)
void TARGET(u16);
#define CALL() TARGET(123)
#elif defined(FORMAL_WORD)
void TARGET(s32);
#define CALL() TARGET(123)
#else
void TARGET(void);
#define CALL() TARGET()
#endif
static void reset(int st,int other,int c,int e,int disable,int busy,u16 p0,u16 p1) {
    n=0;change=c;ready=busy;overlay_value=e;g_system_ptr=&a;g_display_list_head_ptr=gfx;
    a.unk_3add6=st;b.unk_3add6=other;g_system.unk_3add6=other;
    a.stepw=b.stepw=e;a.stepw_end=b.stepw_end=e;g_system.stepw_end=e;
    a.intended_room_id=b.intended_room_id=0;a.intended_room_group_index=b.intended_room_group_index=77;
    a.controller[0].button_pressed=p0;a.controller[1].button_pressed=p1;b.controller[0].button_pressed=b.controller[1].button_pressed=0;
    a.retraces_per_game_step=b.retraces_per_game_step=6;
    g_system.disable_graphics_tasks=disable;g_system.unk_3ae18=0xF123;g_system.current_graphics_pool=-7;
    D_80054B58_55758=busy; D_80161FFC_162BFC=busy?0x1D1:0;
}
int main(void) {
    unsigned cases=0;
    assert(offsetof(SYS_W,current_graphics_pool)==0x3ADB2 && offsetof(SYS_W,disable_graphics_tasks)==0x3ADB6 && offsetof(SYS_W,retraces_per_game_step)==0x3ADCA && offsetof(SYS_W,stepw)==0x3ADD4 && offsetof(SYS_W,stepw_end)==0x3ADD5 && offsetof(SYS_W,unk_3add6)==0x3ADD6 && offsetof(SYS_W,intended_room_id)==0x3ADF2 && offsetof(SYS_W,intended_room_group_index)==0x3ADF4 && offsetof(SYS_W,unk_3ae18)==0x3AE18 && offsetof(SYS_W,controller[0].button_pressed)==0x3B07C && offsetof(SYS_W,controller[1].button_pressed)==0x3B094);
    const int other_vals[]={0,1,127,255}; const int ends[]={0,1,2,3,255}; const int dis[]={0,1,-1};
    const u16 buttons[]={0,0x1000,0x4000,0x8000,0xD000,0xFFFF,0x2000};
#if defined(ROOM_PAIR)
    for(int st=0;st<256;st++)for(int c=0;c<2;c++)for(int v=0;v<4;v++)for(int e=0;e<5;e++)for(int d=0;d<3;d++)for(int busy=0;busy<2;busy++)for(int x=0;x<7;x++)for(int y=0;y<7;y++) {
        int other=other_vals[v],end=ends[e],disable=dis[d];u16 p0=buttons[x],p1=buttons[y];reset(st,other,c,end,disable,busy,p0,p1);CALL();
        if(st==0){check(3,1,2,3,0);assert((c?b:a).intended_room_id==ROOM);assert(a.unk_3add6==(c?0:1));assert(b.unk_3add6==(u8)(other+c));assert(g_system.disable_graphics_tasks==(IS34?0:disable));}
        else if(st==1){check(1,4,0,0,0);int advance=(!IS34||!disable)&&((p0|p1)&BUTTON_MASK);assert(a.stepw_end==(u8)(end+!!advance));assert(b.stepw_end==end);}
        else if(st==2){check(1,5,0,0,0);}
        else if(st==3&&!busy){check(2,1,100+DEST,0,0);assert(g_system.disable_graphics_tasks==(IS34?0:disable));assert(g_system.unk_3ae18==(IS34?0x7123:0xF123));}
        else check(0,0,0,0,0);
        if(st!=0){assert(a.unk_3add6==st && b.unk_3add6==other);}
        if(st!=1)assert(a.stepw_end==end);
        cases++;
    }
#elif defined(COUNT_F0C)
    for(int st=0;st<256;st++)for(int c=0;c<2;c++)for(int v=0;v<4;v++)for(int d=0;d<3;d++)for(int busy=0;busy<2;busy++){
        int other=other_vals[v],disable=dis[d];reset(st,other,c,0,disable,busy,0,0);CALL();
        if(st==0){check(1,15,0,0,0);assert(g_system.disable_graphics_tasks==0&&g_system.unk_3add6==(u8)(other+1));}
        else if(st==1){check(0,0,0,0,0);assert(g_system.disable_graphics_tasks==disable&&g_system.unk_3add6==(u8)(other+1));}
        else if(st==2){check(1,7,0,0,0);assert(g_system.disable_graphics_tasks==(busy?1:disable)&&g_system.unk_3add6==(u8)(other+busy));}
        else if(st==3){check(1,103,0,0,0);assert(g_system.disable_graphics_tasks==disable&&g_system.unk_3add6==other);}
        else {check(0,0,0,0,0);assert(g_system.disable_graphics_tasks==disable&&g_system.unk_3add6==other);}assert(a.unk_3add6==st&&b.unk_3add6==other);cases++;
    }
#elif defined(COUNT_FF4)
    for(int st=0;st<256;st++)for(int c=0;c<2;c++)for(int e=0;e<5;e++)for(int d=0;d<3;d++){
        int end=ends[e],disable=dis[d];reset(st,255,c,end,disable,0,0,0);CALL();
        if(st==0){check(end==3?3:4,22,6,8,9);assert(g_system.disable_graphics_tasks==0);}
        else{check(end==3?2:3,6,8,9,0);assert(g_system.disable_graphics_tasks==disable);}assert(g_display_list_head_ptr==gfx+1&&g_system.unk_3ae18==0x8000);assert((c?b:a).retraces_per_game_step==(end==3?6:2));assert((c?a:b).retraces_per_game_step==6);cases++;
    }
#elif defined(COUNT_658)
    for(int st=0;st<256;st++)for(int c=0;c<2;c++)for(int v=0;v<4;v++)for(int e=0;e<5;e++)for(int busy=0;busy<2;busy++){
        int end=ends[e],other=other_vals[v];reset(st,other,c,end,0,busy,0,0);CALL();
        if(st==0){check(2,1,15,0,0);assert(a.unk_3add6==(c?0:1));assert(b.unk_3add6==(u8)(other+c));}
        else if(st==1){check(1,10,0,0,0);assert(a.intended_room_group_index==0);assert(a.unk_3add6==(c?1:2));assert(b.unk_3add6==(u8)(other+c));}
        else if(st==2){check(end?2:1,11,12,0,0);assert(a.unk_3add6==(end&&!c?3:2));assert(b.unk_3add6==(u8)(other+(end&&c)));}
        else if(st==3&&end){check((end==1||end==2)?2:1,1,end==1?105:busy?109:111,0,0);assert(g_system.unk_3ae18==(end==1?0x8000:0xF123));}
        else check(0,0,0,0,0);cases++;
    }
#endif
    printf("%u actual-source fixture cases PASS\n",cases);
}
