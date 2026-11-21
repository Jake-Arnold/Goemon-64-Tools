#include <assert.h>
#include <stddef.h>
#include <stdio.h>
#include <stdint.h>
#include "jp_gameplay_dispatch.c"
#include "jp_gameplay_teardown.c"
static unsigned char fake_sys[0x3AE20];
u8 *g_system_ptr = fake_sys;
static int called[10], ncalled;
static void initial(void) { called[ncalled++] = 10; }
static void update(void) { called[ncalled++] = 11; }
static void finish(void) { called[ncalled++] = 12; }
Table D_80071210_71E10 = { initial, update, finish };
u32 D_80072E08_73A08 = 0xCAFE1234;
void func_80004170_4D70(void) { called[ncalled++] = 20; }
void func_80034B68_35768(u32 arg0) { assert(arg0 == 0xCAFE1234); called[ncalled++] = 21; }
int main(void) {
  for (int i=0;i<3;i++) {
    fake_sys[0x3ADDE]=(u8)i;
    func_8001F580_20180();
    assert(ncalled==i+1 && called[i]==10+i);
  }
  assert(fake_sys[0x3ADDF]==0);
  func_8001F70C_2030C();
  assert(ncalled==5 && called[3]==20 && called[4]==21);
  assert(fake_sys[0x3ADDF]==1);
  puts("PASS 3/3 dispatch phases, teardown call order, final state write (5 assertions/groups)");
}
