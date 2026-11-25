#include <assert.h>
#include <stdio.h>
#include "common.h"
SYS_W g_system, dynamic[2], *g_system_ptr;
s32 D_80054B58_55758, D_80072E08_73A08 = 73;
static int calls[12], nc, mode;
static void record(int n) { assert(nc<12); calls[nc++]=n; }
void func_80003760_4360(void) { record(1); if(mode&1) g_system_ptr=&dynamic[1]; if(mode&2) g_system.stepw_end=1; }
void func_80020110_20D10(void) { record(2); if(mode&4) g_system_ptr=&dynamic[1]; }
void func_80036624_37224(s32 x) { assert(x==73);record(3); if(mode&8) g_system_ptr=&dynamic[0]; }
s32 func_800364B0_370B0(s32 x) { assert(x==73);record(4);return 0; }
void func_80003808_4408(void) { record(5); }
void func_80003870_4470(void) { record(6); }
void func_8000B550_C150(void) { record(7); }
void func_8000364C_424C(u8 x) { record(100+x); }
void func_80002EF4_3AF4(void);
int main(void) {
    unsigned count=0;
    for(int state=0;state<256;state++)for(int busy=0;busy<2;busy++)for(int end=0;end<4;end++)for(mode=0;mode<16;mode++)for(int boundary=0;boundary<2;boundary++){
        g_system=(SYS_W){.unk_3add6=boundary?255:17,.stepw_end=end,.unk_3ae0c=boundary?255:23,.disable_graphics_tasks=9};
        dynamic[0]=(SYS_W){.unk_3add6=state,.intended_room_group=21,.intended_room_group_index=61};
        dynamic[1]=(SYS_W){.unk_3add6=boundary?255:50,.intended_room_group=22,.intended_room_group_index=62};
        g_system_ptr=dynamic;D_80054B58_55758=busy;nc=0;
        SYS_W exp=g_system,d[2]={dynamic[0],dynamic[1]}; int ptr=0,n=0,e[12];
        switch(state){
        case 0:exp.disable_graphics_tasks=1;exp.unk_3add6=(u8)(exp.unk_3add6+1);break;
        case 1:if(!busy){ e[n++]=1;if(mode&1)ptr=1;if(mode&2)exp.stepw_end=1;d[ptr].intended_room_group=12;d[ptr].intended_room_group_index=0;e[n++]=2;if(mode&4)ptr=1;e[n++]=3;if(mode&8)ptr=0;d[ptr].unk_3add6=(u8)(d[ptr].unk_3add6+1);}break;
        case 2:exp.disable_graphics_tasks=0;e[n++]=4;e[n++]=5;break;
        case 3:e[n++]=6;break;
        case 4:if(!busy){e[n++]=1;if(mode&1)ptr=1;if(mode&2)exp.stepw_end=1;if(exp.stepw_end==1){e[n++]=7;exp.unk_3ae0c=(u8)(exp.unk_3ae0c+1);e[n++]=111;}else e[n++]=103;}break;
        }
        func_80002EF4_3AF4();assert(nc==n);for(int k=0;k<n;k++)assert(e[k]==calls[k]);assert(g_system_ptr==&dynamic[ptr]);
#define CHECK(a,b) do {assert((a).unk_3add6==(b).unk_3add6);assert((a).intended_room_group==(b).intended_room_group);assert((a).stepw_end==(b).stepw_end);assert((a).unk_3ae0c==(b).unk_3ae0c);assert((a).intended_room_group_index==(b).intended_room_group_index);assert((a).disable_graphics_tasks==(b).disable_graphics_tasks);}while(0)
        CHECK(g_system,exp);CHECK(dynamic[0],d[0]);CHECK(dynamic[1],d[1]);count++;
    }printf("PASS %u cases\n",count);return 0;
}
