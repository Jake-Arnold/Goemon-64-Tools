#include <assert.h>
#include <stddef.h>
#include <stdio.h>
#include "jp_transition.h"
SYS_W g_system, a, b, *g_system_ptr;
/* Host-only alias for the actual subobject address; not a production link change. */
__asm__(".globl D_800C24B0\n.set D_800C24B0,g_system+0x30000");
s32 D_80054B58_55758;
u8 D_801D228C[1];
static int events[8], n, change;
s32 D_80072E08_73A08;
static void event(int v) { assert(n<8); events[n++]=v; }
static void check(int count, int first, int second, int third) {
    assert(n==count);
    if(count>0) assert(events[0]==first);
    if(count>1) assert(events[1]==second);
    if(count>2) assert(events[2]==third);
}
static void reset(void) {
    n=change=0; g_system_ptr=&a;
    a.stepw=b.stepw=0; a.unk_3add6=0; b.unk_3add6=255;
    a.intended_room_group_index=b.intended_room_group_index=0;
    g_system.field_adb6=0; g_system.unk_3add6=0; g_system.stepw_end=0;
    g_system.unk_3ae18=0; D_80054B58_55758=0;
}
void func_801D0B90(void) { assert(0); }
void func_80001BA0_27A0(s32 x, void *p) { assert(x==15 && p==(void*)func_801D0B90); event(2); if(change) g_system_ptr=&b; }
void func_80003760_4360(void) { event(1); if(change) g_system_ptr=&b; }
void func_800343A4_34FA4(void) { event(3); }
void func_800344FC_350FC(void *p) { assert(p==D_801D228C); event(4); if(change) g_system_ptr=&b; }
void func_8000364C_424C(u8 x) { event(x==13?13:5); assert(x==13 || x==5); }
void func_8000B120_BD20(void) { event(10); if(change) g_system.unk_3add6=77; }
void func_8000B1E4_BDE4(void) { event(11); if(change) g_system.unk_3add6=77; }
void func_80036660_37260(s32 x) { assert(x==D_80072E08_73A08); event(6); if(change) g_system_ptr=&b; }
void func_80038838_39438(s32 x) { assert(x==7); event(7); }
#ifdef DONOR
void func_80003808_4408(void);
#endif
#ifdef DISPATCHER
void func_80001FE0_2BE0(void);
typedef void (*TransitionHandler)(void);
typedef struct { TransitionHandler handler[18]; } TransitionHandlers;
TransitionHandlers D_80058B88_59788;
#define H(i) static void h##i(void) { event(i); if(change) { g_system_ptr=&b; D_80058B88_59788.handler[i]=0; } }
H(0) H(1) H(2) H(3) H(4) H(5) H(6) H(7) H(8) H(9) H(10) H(11) H(12) H(13) H(14) H(15) H(16) H(17)
static TransitionHandler handlers[18]={h0,h1,h2,h3,h4,h5,h6,h7,h8,h9,h10,h11,h12,h13,h14,h15,h16,h17};
#endif
#ifdef STATE
void func_80003090_3C90(s32);
#endif
#ifdef PAIR
#ifdef FORMAL_BYTE
void TARGET(u8);
#elif defined(FORMAL_INT)
void TARGET(s32);
#else
void TARGET(void);
#endif
#endif
int main(void) {
    unsigned cases=0;
    assert(offsetof(SYS_W,field_adb6)==0x3ADB6 && offsetof(SYS_W,stepw)==0x3ADD4 && offsetof(SYS_W,unk_3add6)==0x3ADD6 && offsetof(SYS_W,intended_room_group_index)==0x3ADF4 && offsetof(SYS_W,unk_3ae18)==0x3AE18);
#ifdef DISPATCHER
    for(int k=0;k<18;k++) for(int c=0;c<2;c++) {
        reset(); change=c; a.stepw=k; for(int i=0;i<18;i++)D_80058B88_59788.handler[i]=handlers[i];
        func_80001FE0_2BE0(); check(1,k,0,0); assert(g_system_ptr==(c?&b:&a)); cases++;
    }
#endif
#ifdef STATE
    for(int st=0;st<256;st++)for(int e=0;e<256;e++)for(int c=0;c<2;c++) {
        reset();change=c;a.unk_3add6=st;g_system.stepw_end=e;func_80003090_3C90(123);
        if(st==0){check(2,1,2,0);assert(a.unk_3add6==(c?0:1));assert(b.unk_3add6==(c?0:255));}
        else if(st==1){check(1,4,0,0);assert(a.intended_room_group_index==3);assert(a.unk_3add6==(c?1:2));assert(b.unk_3add6==(c?0:255));}
        else if(st==2){if(e==0)check(1,3,0,0);else if(e==1||e==2){check(2,1,4,0);assert(g_system.stepw_end==0 && (c?b:a).intended_room_group_index==(e==1?3:1));}else if(e==3){check(2,1,5,0);assert(g_system.unk_3ae18==0x8000);}else check(0,0,0,0);}
        else {check(0,0,0,0);assert(a.unk_3add6==st);}cases++;
    }
#endif
#ifdef PAIR
    const s16 vals[]={0,1,-1,32767,-32768};
    for(int st=0;st<256;st++)for(int v=0;v<5;v++)for(int busy=0;busy<2;busy++)for(int c=0;c<2;c++){
        reset();change=c;g_system.field_adb6=vals[v];g_system.unk_3add6=st;D_80054B58_55758=busy;
#if defined(FORMAL_BYTE) || defined(FORMAL_INT)
        TARGET(123);
#else
        TARGET();
#endif
        if(!st&&!vals[v]) { check(0,0,0,0);assert(g_system.field_adb6==1 && g_system.unk_3add6==1); }
        else if(!busy) { check(3,CALL_ID,1,13);assert(g_system.field_adb6==vals[v] && g_system.unk_3add6==1); }
        else {check(0,0,0,0);assert(g_system.field_adb6==vals[v] && g_system.unk_3add6==st);}cases++;
    }
#endif
#ifdef DONOR
    for(int e=0;e<256;e++)for(int st=0;st<256;st++)for(int c=0;c<2;c++) {
        reset();change=c;g_system.stepw_end=e;a.unk_3add6=b.unk_3add6=st;D_80072E08_73A08=123;
        func_80003808_4408();
        if(e){check(3,3,6,7);assert((c?b:a).unk_3add6==(u8)(st+1));assert((c?a:b).unk_3add6==st);}
        else {check(1,3,0,0);assert(a.unk_3add6==st && b.unk_3add6==st);}
        cases++;
    }
#endif
    printf("%u actual-source fixture cases PASS\n",cases);
    return 0;
}
