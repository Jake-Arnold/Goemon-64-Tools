/* Host-only semantic regression against all 60 actual native-matched C source files. */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

typedef void (*callback_t)(void *,void *);
#define DECL(n) void n(void *,void *)
DECL(func_080003C0_6AC910); DECL(func_08000370_6AC8C0);
DECL(func_080005DC_6ACB2C); DECL(func_0800074C_6ACC9C);
DECL(func_080000C4_6B3064); DECL(func_0800011C_6B30BC); DECL(func_08000268_6B3208);
DECL(func_0800056C_6B380C); DECL(func_08001DB0_6B5050); DECL(func_08001F28_6B51C8);
DECL(func_08001FE8_6B5288); DECL(func_08002460_6B5700); DECL(func_08002864_6B5B04); DECL(func_08002D2C_6B5FCC);
DECL(func_08001488_6C0BD8); DECL(func_080003EC_6CF4CC); DECL(func_080007EC_6CF8CC); DECL(func_0800191C_6D09FC);
static callback_t callback;
static int event_count, finalize_count, init_count, setcb_count;
static unsigned mode_seen, flags_seen, event_id_seen;
static void *actor, *context;
static unsigned char actor_storage[0x120] __attribute__((aligned(16)));
static unsigned char ctx_storage[0x100] __attribute__((aligned(16)));
static uint32_t get32(const void*p,int off){uint32_t x;memcpy(&x,(const char*)p+off,4);return x;}
static void put32(void*p,int off,uint32_t x){memcpy((char*)p+off,&x,4);}
static uint16_t get16(const void*p,int off){uint16_t x;memcpy(&x,(const char*)p+off,2);return x;}
static void put16(void*p,int off,uint16_t x){memcpy((char*)p+off,&x,2);}
static float getfloat(const void*p,int off){float x;memcpy(&x,(const char*)p+off,4);return x;}
static void putfloat(void*p,int off,float x){memcpy((char*)p+off,&x,4);}
static void reset(void){memset(actor_storage,0,sizeof actor_storage);memset(ctx_storage,0,sizeof ctx_storage);actor=actor_storage;context=ctx_storage;callback=0;event_count=finalize_count=init_count=setcb_count=0;mode_seen=flags_seen=event_id_seen=0;}
void func_8003521C_35E1C(callback_t cb){callback=cb;setcb_count++;}
void func_80034ED4_35AD4(void){finalize_count++;}
char D_8020CBF0_5C8B00;
void func_8000F420_10020(uint32_t id,void*global,void*ctx,uint32_t bits){assert(id==0x26e);assert(global==&D_8020CBF0_5C8B00);assert(ctx==context);assert(bits==0x44480000);event_id_seen=id;event_count++;}
void func_802176C4_5D2B94(void*a,unsigned mode){assert(a==actor);mode_seen=mode;event_count++;}
void func_8021664C_5D1B1C(void*a,unsigned v1,unsigned v2,unsigned v3){assert(a==actor);assert(v1==0);flags_seen=v2;mode_seen=v3;init_count++;}
#define STUB_CB(n) void n(void*a,void*b){(void)a;(void)b;}
STUB_CB(func_08000150_6B30F0)
STUB_CB(func_080004E8_6ACA38)
STUB_CB(func_08000434_6CF514)
STUB_CB(func_08000828_6CF908)
STUB_CB(func_080014C8_6C0C18)
STUB_CB(func_08001958_6D0A38)
STUB_CB(func_08001DF0_6B5090)
STUB_CB(func_08001F68_6B5208)
STUB_CB(func_08002028_6B52C8)
STUB_CB(func_08002D6C_6B600C)
int main(void){
 reset(); put32(actor,0xd0,5);put16(context,0x16,10);func_080005DC_6ACB2C(actor,context);assert(get16(context,0x16)==15);
 reset(); put32(actor,0xd0,0x50);put16(context,0x14,0xfff1);func_0800074C_6ACC9C(actor,context);assert(get16(context,0x14)==0x41);
 reset();func_080003C0_6AC910(actor,context);assert(finalize_count==1);
 reset();put32(actor,0x68,0x20);func_080003C0_6AC910(actor,context);assert(finalize_count==0);
 reset();put32(actor,0x68,0x20);putfloat(actor,0x80,4.0f);putfloat(actor,0x78,2.0f);func_08000370_6AC8C0(actor,context);assert(getfloat(actor,0x80)==0.0f && getfloat(actor,0x78)==0.0f);assert(callback==func_080003C0_6AC910);
 reset();func_080000C4_6B3064(actor,context);assert(event_count==0 && setcb_count==0);
 reset();put32(actor,0x68,1);func_080000C4_6B3064(actor,context);assert(event_count==1&&event_id_seen==0x26e && callback==func_0800011C_6B30BC);
 reset();func_0800011C_6B30BC(actor,context);assert(callback==func_08000150_6B30F0);
 reset();put32(actor,0x68,4);func_08000268_6B3208(actor,context);assert(mode_seen==2 && (get32(actor,0x68)&6)==6);
 reset();put16(context,0x16,0x3E0);func_0800056C_6B380C(actor,context);assert(get16(context,0x16)==0x20);
 #define TEST_TIMER(fun,expect_callback) do {reset();put16(actor,0x8A,1);fun(actor,context);assert(get16(actor,0x8A)==0 && callback==0);reset();fun(actor,context);assert(get16(actor,0x8A)==0xFFFF && callback==expect_callback);}while(0)
 TEST_TIMER(func_08001DB0_6B5050,func_08001DF0_6B5090);
 TEST_TIMER(func_08001F28_6B51C8,func_08001F68_6B5208);
 TEST_TIMER(func_08001FE8_6B5288,func_08002028_6B52C8);
 TEST_TIMER(func_08002460_6B5700,func_08002D6C_6B600C);
 TEST_TIMER(func_08002864_6B5B04,func_08002D6C_6B600C);
 TEST_TIMER(func_08002D2C_6B5FCC,func_08002D6C_6B600C);
 reset();put32(actor,0x60,4);func_08001488_6C0BD8(actor,context);assert(get32(actor,0x60)==5&&callback==func_080014C8_6C0C18);
 reset();func_080003EC_6CF4CC(actor,context);assert(init_count==1&&flags_seen==0x3F000000&&mode_seen==1&&callback==func_08000434_6CF514);
 reset();func_080007EC_6CF8CC(actor,context);assert(get16(actor,0x8A)==0x27&&callback==func_08000828_6CF908);
 reset();func_0800191C_6D09FC(actor,context);assert(get16(actor,0x8A)==0x3C&&callback==func_08001958_6D0A38);
 puts("PASS: all 60 matched sources linked; actor angle updates, flag gates, event calls, timer underflow, callbacks, state and init helper semantics");
 return 0;
}
