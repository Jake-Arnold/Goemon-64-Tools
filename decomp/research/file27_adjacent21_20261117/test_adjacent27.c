/* Synthetic host-only regression on the actual original-ID0 C source.
   Does not access the N64 ROM or a running game. */
#include <stdint.h>
#include <assert.h>
#include <stdio.h>
#include <string.h>
#define CB void (*)(void*,void*)
#define FN(f) void f(void*,void*)
FN(func_08000498_6AF8A8); FN(func_080004D4_6AF8E4);
FN(func_0800059C_6AF9AC); FN(func_080005C4_6AF9D4);
FN(func_08000620_6AFA30); FN(func_080008C4_6AFCD4);
FN(func_08000920_6AFD30); FN(func_0800097C_6AFD8C);
FN(func_08000A7C_6AFE8C); FN(func_08000AD8_6AFEE8);
FN(func_08000B34_6AFF44); FN(func_08000B90_6AFFA0);
FN(func_08000BEC_6AFFFC); FN(func_08001380_6B0790);
FN(func_080013C4_6B07D4); FN(func_08001408_6B0818);
FN(func_08001448_6B0858); FN(func_080014A4_6B08B4);
FN(func_0800172C_6B0B3C); FN(func_080037EC_6B2BFC);
void func_08000490_6AF8A0(void*);
static unsigned char actor[0xF0],other[32];
static unsigned logn;
static char logv[256];
static void (*cb)(void*,void*);
static unsigned init_const, trig_param, trail_mode;
static void push(char x){assert(logn+1<sizeof(logv));logv[logn++]=x;logv[logn]=0;}
static void reset(void){logn=0;logv[0]=0;cb=0;init_const=0;trig_param=0;trail_mode=0;}
static void expect(const char*s){if(strcmp(s,logv)){fprintf(stderr,"expected <%s> got <%s>\n",s,logv);assert(0);}}
static uint32_t readw(const void *p,unsigned off){uint32_t x;memcpy(&x,(const char*)p+off,4);return x;}
static void writew(void *p,unsigned off,uint32_t x){memcpy((char*)p+off,&x,4);}
void fake_setup1(void*a){assert(a==actor);push('A');}
void fake_setup2(void*a){assert(a==actor);push('B');}
void fake_repeat(void*a){assert(a==actor);push('R');}
void fake_register(void (*f)(void*,void*)){cb=f;push('K');}
void fake_build(void*a,uint32_t flags){assert(a==actor); init_const=flags;push('I');}
void fake_modulate(void*a,uint32_t b,uint32_t c,uint32_t d){assert(a==actor&&b==0&&c==0x3E800000&&d==1);push('M');}
void fake_end(void){push('E');}
void fake_trigger(void*a,uint32_t arg,void (*next)(void*,void*)){assert(a==actor);assert(arg==0x249);trig_param=arg;cb=next;push('T');}
void fake_unused0(void *a,void *b) { (void)a;(void)b; }
void fake_unused1(void *a,void *b) { (void)a;(void)b; }
uint32_t D_8005B1A4=0;
#define ALIAS(s,f) __asm__(".globl " #s "\n.set " #s ", " #f "\n")
ALIAS(func_80221A90_5DCF60,fake_setup1);
ALIAS(func_80220F70_5DC440,fake_setup2);
ALIAS(func_802213F4_5DC8C4,fake_repeat);
ALIAS(func_8003521C_35E1C,fake_register);
ALIAS(func_080004FC_6AF90C,fake_build);
ALIAS(func_80221C0C_5DD0DC,fake_modulate);
ALIAS(func_80221FB0_5DD480,fake_end);
ALIAS(func_80221638_5DCB08,fake_trigger);
ALIAS(func_080012C0_6B06D0,fake_unused0);
ALIAS(func_08001568_6B0978,fake_unused1);
static void (*wrappers[])(void*,void*)={
 func_080005C4_6AF9D4,func_080008C4_6AFCD4,func_08000920_6AFD30,func_0800097C_6AFD8C,
 func_08000A7C_6AFE8C,func_08000AD8_6AFEE8,func_08000B34_6AFF44,func_08000B90_6AFFA0,func_08001448_6B0858};
int main(void){
 memset(actor,0,sizeof actor);
 reset();func_08000490_6AF8A0(actor);expect("");
 reset();func_08000498_6AF8A8(actor,other);expect("AK");assert(cb==func_080004D4_6AF8E4);
 reset();func_080004D4_6AF8E4(actor,other);expect("B");
 reset();func_0800059C_6AF9AC(actor,other);func_08000620_6AFA30(actor,other);expect("RR");
 for (unsigned i=0;i<sizeof(wrappers)/sizeof(wrappers[0]);i++){
  reset();wrappers[i](actor,other);expect("IMK");assert(cb==func_0800059C_6AF9AC);
  assert(init_const==(i==0||i==7||i==8 ? 0x10000661u : 0x12800761u));
 }
 reset();func_08000BEC_6AFFFC(actor,other);func_080014A4_6B08B4(actor,other);func_080037EC_6B2BFC(actor,other);expect("");
 writew(actor,0xD0,22);D_8005B1A4=7;
 reset();func_08001380_6B0790(actor,other);expect("K");assert(D_8005B1A4==0);assert(readw(actor,0xD0)==15);assert(cb==func_080013C4_6B07D4);
 reset();func_080013C4_6B07D4(actor,other);expect("");assert(readw(actor,0xD0)==14);
 writew(actor,0xD0,0);reset();func_080013C4_6B07D4(actor,other);expect("T");assert(readw(actor,0xD0)==0xFFFFFFFFu);assert(trig_param==0x249);assert(cb==func_08001408_6B0818);
 reset();func_08001408_6B0818(actor,other);expect("EK");assert(cb==fake_unused0);
 reset();func_0800172C_6B0B3C(actor,other);expect("EK");assert(cb==fake_unused1);
 puts("PASS: 21 actual original-ROM-matched resource27 C functions, callback/timer/wrapper branches");
 return 0;
}
