#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned char u8;
typedef void (*DispatchFn)(void);
typedef struct DispatchTable { DispatchFn callbacks[18]; } DispatchTable;
extern void func_80002040_2C40(void);

static unsigned call_count, last_handler;
static void callback0(void) { call_count++; last_handler=0; }
static void callback1(void) { call_count++; last_handler=1; }
static void callback2(void) { call_count++; last_handler=2; }
static void callback3(void) { call_count++; last_handler=3; }
static void callback4(void) { call_count++; last_handler=4; }
static void callback5(void) { call_count++; last_handler=5; }
static void callback6(void) { call_count++; last_handler=6; }
static void callback7(void) { call_count++; last_handler=7; }
static void callback8(void) { call_count++; last_handler=8; }
static void callback9(void) { call_count++; last_handler=9; }
static void callback10(void) { call_count++; last_handler=10; }
static void callback11(void) { call_count++; last_handler=11; }
static void callback12(void) { call_count++; last_handler=12; }
static void callback13(void) { call_count++; last_handler=13; }
static void callback14(void) { call_count++; last_handler=14; }
static void callback15(void) { call_count++; last_handler=15; }
static void callback16(void) { call_count++; last_handler=16; }
static void callback17(void) { call_count++; last_handler=17; }
const DispatchTable D_80058908_59508={{callback0,callback1,callback2,callback3,callback4,callback5,callback6,callback7,callback8,callback9,callback10,callback11,callback12,callback13,callback14,callback15,callback16,callback17}};
u8* D_8015C5C8_15D1C8;
int main(void){
  static u8 system_state[0x3ADD5];
  unsigned i,repetition;
  D_8015C5C8_15D1C8=system_state;
  for(repetition=0;repetition<3;repetition++){
    for(i=0;i<18;i++){
      unsigned previous=call_count;
      system_state[0x3ADD4]=(u8)i;
      func_80002040_2C40();
      assert(call_count==previous+1);
      assert(last_handler==i);
    }
  }
  assert(call_count==54);
  printf("PASS 54 valid-state dispatches across 18 handlers\n");
  return 0;
}
