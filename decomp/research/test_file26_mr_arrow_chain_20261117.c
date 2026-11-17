/* Host ABI contract tests for real resource-26 candidate C, no ROM assets. */
#include <assert.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>

typedef void (*Callback)(void*,void*);
void func_080000CC_6AE8AC(void*,void*);
void func_08000174_6AE954(void*,void*);
void func_080001B4_6AE994(void*,void*);
static char events[64];
static int event_count;
static Callback callback;
static int query_return;
static void *expected_actor;
static void *expected_context;
static void push(char c){ assert(event_count < 63); events[event_count++]=c; events[event_count]=0; }

void fake_begin(void){ push('B'); }
void fake_event(uint32_t n){ assert(n==0x6C); push('E'); }
void fake_cleanup(void *actor,unsigned a,unsigned b,unsigned c){ assert(actor==expected_actor); assert(a==0&&b==0&&c==0); push('C'); }
void fake_sync(void *actor){ assert(actor==expected_actor); push('S'); }
void fake_saved(unsigned short flag){ assert(flag==0x104); push('F'); }
void fake_callback(Callback cb){ callback=cb; push('K'); }
void fake_transition(void *actor,unsigned n){ assert(actor==expected_actor);assert(n==0); push('T'); }
int fake_query(void){ push('Q'); return query_return; }
void fake_finalize0(void){ push('R'); }
void fake_finalize1(void){ push('L'); }

#define ALIAS(symbol,target) __asm__(".globl " #symbol "\n.set " #symbol ", " #target "\n")
ALIAS(func_80221F70_5DD440,fake_begin);
ALIAS(func_8003D310_3DF10,fake_event);
ALIAS(func_80218DA8_5D4278,fake_cleanup);
ALIAS(func_8021A22C_5D56FC,fake_sync);
ALIAS(func_80024038_24C38,fake_saved);
ALIAS(func_8003521C_35E1C,fake_callback);
ALIAS(func_8021804C_5D351C,fake_transition);
ALIAS(func_8003F1D8_3FDD8,fake_query);
ALIAS(func_80221FB0_5DD480,fake_finalize0);
ALIAS(func_80034ED4_35AD4,fake_finalize1);

static void set_u16(unsigned char *p, unsigned short v){ memcpy(p,&v,sizeof(v)); }
static void set_u32(unsigned char *p, uint32_t v){ memcpy(p,&v,sizeof(v)); }
static uint32_t get_u32(const unsigned char *p){ uint32_t v;memcpy(&v,p,sizeof(v));return v; }
static void reset(void){ memset(events,0,sizeof events); event_count=0; }
static void expect(const char *s){ if (strcmp(events,s)) {fprintf(stderr,"expected %s got %s\n",s,events); assert(0);} }
int main(void){
    union { unsigned long long alignment; unsigned char bytes[0xE0]; } a;
    unsigned char ctx[4]={0};
    memset(&a,0,sizeof(a)); expected_actor=a.bytes; expected_context=ctx;
    set_u16(a.bytes+0xD0,0x104); set_u32(a.bytes+0x60,0xABCD1234);
    reset(); func_080000CC_6AE8AC(a.bytes,ctx); expect(""); assert(get_u32(a.bytes+0x60)==0xABCD1234);
    set_u32(a.bytes+0x68,0x200); reset(); func_080000CC_6AE8AC(a.bytes,ctx);
    expect("BECSFK");assert(get_u32(a.bytes+0x60)==0);assert(callback==func_08000174_6AE954);
    reset(); callback(a.bytes,ctx); expect("TK"); assert(callback==func_080001B4_6AE994);
    query_return=1; reset(); callback(a.bytes,ctx); expect("Q");
    query_return=0; reset(); callback(a.bytes,ctx); expect("QRL");
    puts("PASS: actual resource-26 C callbacks, bit gate, flag ID, transition chain, both completion branches");
    return 0;
}
