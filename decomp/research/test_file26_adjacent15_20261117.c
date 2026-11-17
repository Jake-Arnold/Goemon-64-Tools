/* Host tests for real resource26 matching-C source. No ROM or game assets. */
#include <assert.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>

/* No hidden `actor` struct layout assumptions: unsigned byte offsets from original MIPS. */
#define FN(n) void n(void *, void *)
FN(func_08000000_6AE7E0); FN(func_080000CC_6AE8AC); FN(func_08000174_6AE954); FN(func_080001B4_6AE994);
FN(func_08000204_6AE9E4); FN(func_080002D0_6AEAB0); FN(func_08000378_6AEB58); FN(func_08000434_6AEC14);
FN(func_080004AC_6AEC8C); FN(func_08000514_6AECF4); FN(func_080005F8_6AEDD8); FN(func_080006E0_6AEEC0);
FN(func_08000740_6AEF20); FN(func_0800083C_6AF01C); FN(func_080009F4_6AF1D4);
typedef void (*CB)(void *,void *);
static void *actor, *ctx, *child;
static CB callback;
static char logbuf[256];
static unsigned nlog;
static unsigned check_result, query_result, expected_event, expected_mode;
static void push(char c){assert(nlog<255);logbuf[nlog++]=c;logbuf[nlog]=0;}
static void reset(void){memset(logbuf,0,sizeof(logbuf));nlog=0;callback=0;}
static void expect(const char *s){if(strcmp(logbuf,s)!=0){fprintf(stderr,"Expected <%s> got <%s>\n",s,logbuf);assert(0);}}
static unsigned u32at(const void *p,int off){unsigned x;memcpy(&x,(const char*)p+off,4);return x;}
static void put32(void*p,int off,unsigned x){memcpy((char*)p+off,&x,4);}
static unsigned short u16at(const void *p,int off){unsigned short x;memcpy(&x,(const char*)p+off,2);return x;}
static void put16(void*p,int off,unsigned short x){memcpy((char*)p+off,&x,2);}
static void putptr(void*p,int off,void*x){memcpy((char*)p+off,&x,sizeof(x));}
int fake_check(unsigned short id){assert(id==0x104 || id==0xE2);push('G');return (int)check_result;}
void fake_init1(void *a,unsigned b,unsigned c,unsigned d){assert(a==actor);assert((b==500 && c==50) || (b==0&&c==0)); assert(d==0);push('C');}
void fake_init2(void *a,unsigned mode){assert(a==actor);assert(mode==expected_mode);if(mode==1 || mode==2){assert(u16at(a,0x5E)==1);}push('T');}
void fake_init3(void *a,unsigned b,unsigned c){assert(a==actor&&b==8&&c==0);push('P');}
void fake_init4(void *a){assert(a==actor);push('R');}
void fake_set_cb(CB cb){callback=cb;push('K');}
void *fake_direct(void *a,unsigned mode){assert(a==actor);assert(mode<=1);push('D');return child;}
void fake_begin(void){push('B');}
void fake_event(unsigned id){assert(id==expected_event);push('E');}
void fake_sync(void *a){assert(a==actor);push('S');}
void fake_saved(unsigned short id){assert(id==0x104);push('F');}
void fake_query_log0(unsigned id){assert(id==0x26C);push('X');}
void fake_query_log1(unsigned id){assert(id==0x28);push('Y');}
int fake_query(void){push('Q');return (int)query_result;}
void fake_done1(void){push('H');}
void fake_done2(void){push('L');}
void fake_done3(void){push('M');}
/* ELF link-time aliases retain the C candidate's unchanged MIPS symbol spellings. */
#define ALIAS(sym,fake) __asm__(".globl "#sym"\n.set "#sym", "#fake"\n")
ALIAS(func_800240DC_24CDC,fake_check);
ALIAS(func_80218DA8_5D4278,fake_init1);
ALIAS(func_80216E1C_5D22EC,fake_init2);
ALIAS(func_80219E70_5D5340,fake_init3);
ALIAS(func_8021A310_5D57E0,fake_init4);
ALIAS(func_8003521C_35E1C,fake_set_cb);
ALIAS(func_8021804C_5D351C,fake_direct);
ALIAS(func_80221F70_5DD440,fake_begin);
ALIAS(func_8003D310_3DF10,fake_event);
ALIAS(func_8021A22C_5D56FC,fake_sync);
ALIAS(func_80024038_24C38,fake_saved);
ALIAS(func_80038B98_39798,fake_query_log0);
ALIAS(func_801DCD48_598C58,fake_query_log1);
ALIAS(func_8003F1D8_3FDD8,fake_query);
ALIAS(func_8000B824_C424,fake_done1);
ALIAS(func_80221FB0_5DD480,fake_done2);
ALIAS(func_80034ED4_35AD4,fake_done3);

static void fresh(void){
 static _Alignas(8) unsigned char actor_storage[0x160];
 static unsigned char child_storage[0x110];
 static unsigned char ctx_storage[0xA0];
 memset(actor_storage,0,sizeof(actor_storage));memset(child_storage,0,sizeof(child_storage));memset(ctx_storage,0,sizeof(ctx_storage));
 /* N64 pointer fields are 4-byte aligned; choose test actor base to align
  * actor+0xE4 for host 64-bit pointer width, without modifying candidate C. */
 actor=actor_storage+4;
 child=child_storage;
 ctx=ctx_storage;
 put16(actor,0xD0,0x104);
 put16(actor,0x5E,0x1234);
 putptr(actor,0xE4,child);
 check_result=0;query_result=0;expected_mode=0;expected_event=0;
 reset();
}
int main(void){
 fresh();check_result=1;func_08000000_6AE7E0(actor,ctx);expect("G");assert(u32at(actor,0x68)==2);
 fresh();func_08000000_6AE7E0(actor,ctx);expect("GCTPRK");assert(u32at(actor,0x60)==0x4006E0);assert(((unsigned char*)actor)[0x4C]==8);assert(callback==func_080000CC_6AE8AC);
 fresh();func_08000204_6AE9E4(actor,ctx);expect("GCTPRK");assert(callback==func_080002D0_6AEAB0);
 fresh();put32(actor,0x68,0x200);expected_event=0x6C;func_080000CC_6AE8AC(actor,ctx);expect("BECSFK");assert(callback==func_08000174_6AE954);
 fresh();put32(actor,0x68,0x200);expected_event=0x6B;func_080002D0_6AEAB0(actor,ctx);expect("BECSFK");assert(u32at(actor,0x60)==0);assert(callback==func_08000174_6AE954);
 fresh();func_08000174_6AE954(actor,ctx);expect("DK");assert(callback==func_080001B4_6AE994);
 fresh();query_result=1;func_080001B4_6AE994(actor,ctx);expect("Q");
 fresh();func_080001B4_6AE994(actor,ctx);expect("QLM");
 fresh();func_08000378_6AEB58(actor,ctx);expect("CTPRDK");assert(u32at(actor,0x60)==0x4006E0);assert(callback==func_08000434_6AEC14);assert(((unsigned char*)actor)[0x4C]==7);
 fresh();func_08000434_6AEC14(actor,ctx);expect("");
 fresh();put32(actor,0x68,0x200);put32(actor,0x60,0xFFFFFFFF);func_08000434_6AEC14(actor,ctx);expect("XYK");assert(u32at(actor,0x60)==0xF7FFFFFF);assert(callback==func_080004AC_6AEC8C);
 fresh();func_080004AC_6AEC8C(actor,ctx);expect("DLM");assert(((unsigned char*)child)[0xD0]==1);
 fresh();expected_mode=2;func_08000514_6AECF4(actor,ctx);expect("GCTPRK");assert(u16at(actor,0x5E)==0x1234);assert(callback==func_080005F8_6AEDD8);
 fresh();expected_event=0x66;put32(actor,0x68,0x200);func_080005F8_6AEDD8(actor,ctx);expect("BDFGECSK");assert(callback==func_080006E0_6AEEC0);
 fresh();expected_event=0x312;check_result=1;put32(actor,0x68,0x200);func_080005F8_6AEDD8(actor,ctx);expect("BDFGECSK");
 fresh();query_result=1;func_080006E0_6AEEC0(actor,ctx);expect("Q");
 fresh();func_080006E0_6AEEC0(actor,ctx);expect("QHLM");
 fresh();expected_mode=1;func_08000740_6AEF20(actor,ctx);expect("GCTPRDK");assert(u16at(actor,0x5E)==0x1234);assert(callback==func_0800083C_6AF01C);
 fresh();expected_event=0x6A;put32(actor,0x68,0x200);func_0800083C_6AF01C(actor,ctx);expect("BDECSFK");assert(((unsigned char*)child)[0xD0]==1);assert(callback==func_080006E0_6AEEC0);
 fresh();put16(ctx,0x16,0x3FE);func_080009F4_6AF1D4(actor,ctx);expect("");assert(u16at(ctx,0x16)==2);
 fresh();put16(ctx,0x16,0x3FE);put32(actor,0x68,0x200);expected_event=0x64;func_080009F4_6AF1D4(actor,ctx);expect("BECSFK");assert(u16at(ctx,0x16)==2);assert(((unsigned char*)child)[0xD0]==1);assert(callback==func_080004AC_6AEC8C);
 puts("PASS resource26 15 exact C functions: actor gate, branch events, callbacks, child state, temporary restore");
 return 0;
}
