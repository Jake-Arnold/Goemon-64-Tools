#include <assert.h>
#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>

typedef unsigned int u32;
typedef unsigned short u16;
typedef struct {char pad0[8];u32 position[3];u16 rotation[3];u16 pad1;float translation[3];} Pose;
extern void func_8001E2BC_1EEBC(void*, Pose*);
extern void func_8001E380_1EF80(void*, Pose*);
u16 D_801689F0_1695F0, D_801689F2_1695F2, D_801689F4_1695F4;
struct Capture {void *ctx;u32 p[3];u16 r[3];float t[3];unsigned calls;};
static struct Capture cap1,cap2;
static void record(struct Capture *cap,void *ctx,u32 p0,u32 p1,u32 p2,u16 r0,u16 r1,u16 r2,float t0,float t1,float t2) {
 cap->ctx=ctx;cap->p[0]=p0;cap->p[1]=p1;cap->p[2]=p2;
 cap->r[0]=r0;cap->r[1]=r1;cap->r[2]=r2;
 cap->t[0]=t0;cap->t[1]=t1;cap->t[2]=t2;cap->calls++;
}
void func_8001E9B0_1F5B0(void*ctx,u32 p0,u32 p1,u32 p2,u16 r0,u16 r1,u16 r2,float t0,float t1,float t2) {
 record(&cap1,ctx,p0,p1,p2,r0,r1,r2,t0,t1,t2);
}
void func_8001EC04_1F804(void*ctx,u32 p0,u32 p1,u32 p2,u16 r0,u16 r1,u16 r2,float t0,float t1,float t2) {
 record(&cap2,ctx,p0,p1,p2,r0,r1,r2,t0,t1,t2);
}
static void check_capture(struct Capture *c,void *ctx,Pose *p) {
 unsigned i;assert(c->calls==1 && c->ctx==ctx);
 for (i=0;i<3;i++) {
  assert(c->p[i]==p->position[i]);
  assert(c->r[i]==p->rotation[i]);
  assert(c->t[i]==p->translation[i]);
 }
}
static void test_wrappers(void) {
 Pose p;int marker=3;
 assert(offsetof(Pose,position)==0x8);
 assert(offsetof(Pose,rotation)==0x14);
 assert(offsetof(Pose,translation)==0x1C);
 memset(&p,0,sizeof p);
 for(unsigned i=0;i<3;i++) {p.position[i]=0x50000000u+i*0x1F03;p.rotation[i]=(u16)(i*0x123);p.translation[i]=i*1.5f-2.0f;}
 p.rotation[0]=0x8000;p.rotation[1]=0x123;p.rotation[2]=0x8000;
 func_8001E2BC_1EEBC(&marker,&p); check_capture(&cap1,&marker,&p);
 assert(D_801689F0_1695F0==0 && D_801689F2_1695F2==0x123 && D_801689F4_1695F4==0);
 func_8001E380_1EF80(&marker,&p); check_capture(&cap2,&marker,&p);
 p.rotation[0]=0x3ff;p.rotation[1]=0x8000;p.rotation[2]=0x7fff;
 memset(&cap1,0,sizeof cap1);
 func_8001E2BC_1EEBC(&marker,&p);check_capture(&cap1,&marker,&p);
 assert(D_801689F0_1695F0==0x3ff && D_801689F2_1695F2==0 && D_801689F4_1695F4==0x7fff);
}
int main(void) {test_wrappers();puts("pose wrapper semantics: PASS");return 0;}
