#include <assert.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include "transition.h"
TransitionStatic D_800BCCC0_BD8C0;
s32 D_800548D8_554D8, D_8006D328_6DF28;
u8 D_801CCB7C[1];
static SYS_W sys[2];
SYS_W *D_8015C5C8_15D1C8;
static char logbuf[16];
static unsigned n;
static s32 result;
static int swap;
static void event(char c) { assert(n < sizeof(logbuf)); logbuf[n++]=c; }
void func_801CB460(void) {}
void func_80001C00_2800(s32 id, void *p) { assert(id==15 && p==(void *)func_801CB460); event('L'); }
void func_8000383C_443C(void) { event('C'); if(swap) D_8015C5C8_15D1C8=&sys[1]; }
void func_80003880_4480(void) { event('R'); assert(D_800BCCC0_BD8C0.field_b01d==5 && D_800BCCC0_BD8C0.field_adb6==1); if(swap) D_8015C5C8_15D1C8=&sys[1]; }
void func_80034734_35334(void) { event('T'); }
void func_8003488C_3548C(void *p) { assert(p==D_801CCB7C); event('A'); }
void func_80003728_4328(u8 s) { assert(s==5); event('S'); }
s32 func_80036908_37508(s32 v) { assert(v==D_8006D328_6DF28); event('Q'); return result; }
void func_8000394C_454C(void);
void func_800030F0_3CF0(s32);
static void reset(void) { memset(&D_800BCCC0_BD8C0,0,sizeof(D_800BCCC0_BD8C0)); memset(sys,0,sizeof(sys)); memset(logbuf,0,sizeof(logbuf)); n=0; result=0; swap=0; D_800548D8_554D8=0; D_8006D328_6DF28=123; D_8015C5C8_15D1C8=&sys[0]; }
static void checklog(const char *s) { assert(n==strlen(s)); assert(memcmp(s,logbuf,n)==0); }
int main(void) {
    unsigned i,j,cases=0;
    assert(offsetof(TransitionStatic, field_adb6)==0xADB6 && offsetof(TransitionStatic, field_add5)==0xADD5 && offsetof(TransitionStatic, field_add6)==0xADD6 && offsetof(TransitionStatic, field_ae18)==0xAE18 && offsetof(TransitionStatic, field_b01d)==0xB01D);
    for(i=0;i<256;i++) for(j=0;j<2;j++) {
        reset(); result=(s32)j; sys[0].unk_3add6=(u8)i; func_8000394C_454C(); checklog(j?"TQ":"TQR"); assert(sys[0].unk_3add6==(u8)(i+!j)); assert(D_800BCCC0_BD8C0.field_b01d==(j?0:5)); assert(D_800BCCC0_BD8C0.field_adb6==(j?0:1)); cases++;
    }
    reset(); swap=1; sys[0].unk_3add6=7; sys[1].unk_3add6=255; func_8000394C_454C(); checklog("TQR"); assert(sys[0].unk_3add6==7 && sys[1].unk_3add6==0); cases++;
    for(i=0;i<256;i++) for(j=0;j<256;j++) {
        reset(); D_800BCCC0_BD8C0.field_add6=(u8)i; D_800BCCC0_BD8C0.field_add5=(u8)j; sys[0].unk_3add6=255; D_800BCCC0_BD8C0.field_adb6=7;
        func_800030F0_3CF0((s32)(i * 257u + j));
        if(i==0) { checklog(""); assert(D_800BCCC0_BD8C0.field_adb6==1 && D_800BCCC0_BD8C0.field_add6==1 && D_800BCCC0_BD8C0.field_add5==0); }
        else if(i==1) { checklog("CL"); assert(sys[0].unk_3add6==0); }
        else if(i==2) { checklog(""); assert(sys[0].unk_3add6==0 && D_800BCCC0_BD8C0.field_adb6==0); }
        else if(i==3) { checklog("A"); assert(sys[0].unk_3add6==0 && sys[0].intended_room_group_index==3); }
        else if(i==4) { switch(j) { case 0: checklog("T"); break; case 1: case 2: checklog("CA"); assert(sys[0].intended_room_group_index==(j==1?3:1)); assert(D_800BCCC0_BD8C0.field_add5==0); break; case 3: checklog("CS"); assert(D_800BCCC0_BD8C0.field_ae18==0x8000); break; default: checklog(""); } }
        else { checklog(""); assert(sys[0].unk_3add6==255 && D_800BCCC0_BD8C0.field_add6==i && D_800BCCC0_BD8C0.field_add5==j); }
        cases++;
    }
    reset(); D_800BCCC0_BD8C0.field_add6=1; D_800548D8_554D8=1; func_800030F0_3CF0((s32)(i * 257u + j)); checklog(""); assert(sys[0].unk_3add6==0); cases++;
    reset(); D_800BCCC0_BD8C0.field_add6=1; swap=1; sys[0].unk_3add6=2; sys[1].unk_3add6=7; func_800030F0_3CF0((s32)(i * 257u + j)); checklog("CL"); assert(sys[0].unk_3add6==2 && sys[1].unk_3add6==8); cases++;
    printf("%u actual-source semantic cases PASS\n",cases); return 0;
}
