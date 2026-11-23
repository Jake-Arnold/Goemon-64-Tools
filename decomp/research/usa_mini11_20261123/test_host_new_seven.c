/* Bounded host-side checks of the actual seven reconstructed C bodies.
 * Original MIPS symbols and game memory are NOT provided here.
 * Pointers are aligned for the host (task base +4 makes +0x5C 8-byte aligned).
 */
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>
typedef unsigned char u8;
typedef unsigned short u16;
typedef float f32;
extern void func_801E2180_59E090(void *);
extern void func_801E2220_59E130(void *);
extern void func_801E2800_59E710(void *,u8);
extern void func_801E2AA0_59E9B0(void *);
extern void func_801E2BA8_59EAB8(void *);
extern void func_801E2CEC_59EBFC(void *,u8);
extern void func_801E2D74_59EC84(void *,u8,u8);
f32 D_8020B30C_5C721C = 9.0f;
f32 D_8020B310_5C7220 = 16.0f;
f32 D_8020B314_5C7224 = 0.5f;
f32 D_8020B318_5C7228 = 3.25f;
void *D_8015CCC0_15D8C0 = (void*)0x123456;
static int predicate, pred_calls, state_calls, audio_calls, pose_calls, effect_calls, event_calls;
static int last_state,last_audio,last_pose,last_effect,last_event;
static void *effect_return;
int func_801E7DE8_5A3CF8(void *a) {(void)a;pred_calls++;return predicate;}
void func_801DD830_599740(void *a,int b) {(void)a;state_calls++;last_state=b;}
void func_80038BC8_397C8(int a) {audio_calls++;last_audio=a;}
void func_801DD6E0_5995F0(void *a,int b) {(void)a;event_calls++;last_event=b;}
void func_801E3834_59F744(void *a,int b) {(void)a;pose_calls++;last_pose=b;}
void func_801E8964_5A4874(void *a,u8 b) {(void)a;event_calls++;last_event=b;}
void *func_801DB494_5973A4(void *a,void *b,int c,int d,f32 e) {
    (void)a;
    if(b!=D_8015CCC0_15D8C0 || c!=0x196 || d!=0x80 || e!=115.0f) abort();
    effect_calls++;return effect_return;
}
#define CHECK(cond) do {if(!(cond)){fprintf(stderr,"FAIL line %d: %s\n",__LINE__,#cond);abort();}}while(0)
static void wr_f(void *a,int off,f32 val){memcpy((u8*)a+off,&val,4);}
static f32 rd_f(void *a,int off){f32 v;memcpy(&v,(u8*)a+off,4);return v;}
static void wr_u16(void *a,int off,u16 val){memcpy((u8*)a+off,&val,2);}
static u16 rd_u16(void *a,int off){u16 v;memcpy(&v,(u8*)a+off,2);return v;}
static void wr_ptr(void *a,int off,void *p){memcpy((u8*)a+off,&p,sizeof(p));}
static void *rd_ptr(void *a,int off){void *p;memcpy(&p,(u8*)a+off,sizeof(p));return p;}
int main(void){
    _Alignas(16) u8 taskmem[640],ctxmem[480],altmem[160];
    void *task=taskmem+4,*ctx=ctxmem;
    for(int i=0;i<8192;i++){
        memset(taskmem,0x5a,sizeof(taskmem));memset(ctxmem,0x5a,sizeof(ctxmem));
        wr_ptr(task,0x5C,ctx);
        predicate = i&1; pred_calls=state_calls=audio_calls=event_calls=pose_calls=effect_calls=0;
        /* Two-call state-dependent sqrt and staged movement fields. */
        wr_f(task,0xA4,-9.0f);wr_f(task,0x6C,8.0f);wr_u16(ctx,0x30,0x1234);((u8*)ctx)[0x2E]=77;
        func_801E2180_59E090(task);
        CHECK(pred_calls==2 && state_calls==1 && last_state==1);
        CHECK(rd_f(task,0xA4)==(predicate?sqrtf(9.0f):sqrtf(16.0f))+0.5f);
        CHECK(rd_f(task,0x6C)==0.0f && rd_u16(ctx,0x30)==0 && ((u8*)ctx)[0x2E]==0);
        CHECK((predicate && audio_calls==1 && last_audio==0x2B5) || (!predicate && event_calls==1 && last_event==0x21));
        /* Positive-zero reset and two context flags. */
        wr_f(task,0xA4,-1.0f);wr_f(task,0x6C,5.0f);wr_u16(ctx,0x30,0xffff);((u8*)ctx)[0x2E]=9;
        state_calls=0;func_801E2220_59E130(task);
        CHECK(state_calls==1 && last_state==1 && rd_f(task,0xA4)==3.25f && rd_f(task,0x6C)==0.0f);
        CHECK(rd_u16(ctx,0x30)==0 && ((u8*)ctx)[0x2E]==0);
        /* Plain movement reset and masked event value. */
        ((u8*)task)[0x30]=(u8)(i&255); wr_f(task,0xE4,13.0f);wr_f(task,0xE8,14.0f);
        event_calls=0;func_801E2CEC_59EBFC(task,(u8)(i&255));
        CHECK(((u8*)task)[0x30]==((i&255)&~1) && rd_f(task,0xE4)==0.0f && rd_f(task,0xE8)==0.0f);
        CHECK(event_calls==1 && last_event==(i&255));
        /* Common 3D velocity norm and its two wrappers. */
        f32 x=(f32)((i%17)-8),y=(f32)((i%19)-9),z=(f32)((i%13)-6);
        for(int variant=0;variant<3;variant++){
            wr_f(task,0x68,x);wr_f(task,0x6C,y);wr_f(task,0x70,z);
            wr_f(task,0xE4,-3.0f);wr_f(task,0xE8,4.0f);
            wr_u16(ctx,0,0);wr_u16(ctx,2,0);wr_u16(ctx,8,0x0123);wr_u16(ctx,0x1A,0x0045);
            ((u8*)ctx)[0x2C]=0xA5;
            pose_calls=event_calls=0;
            if(variant==0)func_801E2800_59E710(task,(u8)(i&255));
            if(variant==1)func_801E2BA8_59EAB8(task);
            if(variant==2)func_801E2D74_59EC84(task,(u8)(i&255),(u8)((i+23)&255));
            f32 expected=sqrtf(z*z+(x*x+y*y))/2;
            CHECK(pose_calls==1 && last_pose==(variant==1?15:(i&255)));
            CHECK(rd_f(task,0x68)==0.0f && rd_f(task,0x6C)==0.0f && rd_f(task,0x70)==0.0f);
            CHECK(rd_f(task,0xE4)==expected && rd_f(task,0xE8)==1.0f && rd_f(ctx,4)==expected);
            CHECK(rd_u16(ctx,0)==1 && ((u8*)ctx)[0x2C]==0);
            CHECK(rd_u16(ctx,2)==((variant==1?0x45:0x123)|0x400));
            CHECK(event_calls==(variant==2) && (variant!=2 || last_event==((i+23)&255)));
        }
        /* Allocation/reset on both null and non-null branches. */
        effect_return=(i&1)?NULL:altmem;wr_ptr(ctx,0x88,(void*)0);wr_u16(ctx,0x34,0xAAAA);
        wr_f(task,0xE4,-2.0f);wr_f(task,0xE8,-3.0f);
        wr_f(task,0x68,4.0f);wr_f(task,0x6C,5.0f);wr_f(task,0x70,6.0f);
        ((u8*)ctx)[0x2C]=0xff;wr_u16(ctx,0x30,0x1234);
        state_calls=effect_calls=0;func_801E2AA0_59E9B0(task);
        CHECK(state_calls==1 && last_state==4 && effect_calls==1 && rd_ptr(ctx,0x88)==effect_return);
        CHECK(rd_u16(ctx,0x34)==0 && rd_f(task,0xE4)==0.0f && rd_f(task,0xE8)==0.0f);
        CHECK(rd_f(task,0x68)==0.0f && rd_f(task,0x6C)==0.0f && rd_f(task,0x70)==0.0f);
        if(effect_return==NULL) CHECK(((u8*)ctx)[0x2C]==0 && rd_u16(ctx,0x30)==0);
        else CHECK(((u8*)ctx)[0x2C]==0xff && rd_u16(ctx,0x30)==0x1234);
    }
    puts("SEVEN_ORIGINAL_C_HOST_SANITIZERS_PASS 8192_STATES 65536_FUNCTION_CALLS");
    return 0;
}
