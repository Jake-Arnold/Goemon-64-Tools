#include <assert.h>
#include <stdio.h>
#include "usa_gameplay_dispatch.c"
static unsigned char synthetic[0x3AE20];
u8 *g_system_ptr=synthetic;
static int called;
static void a(void) { called = 1; }
static void b(void) { called = 2; }
static void c(void) { called = 3; }
Table D_8006B730_6C330 = {a,b,c};
int main(void) { for(int i=0;i<3;i++) { synthetic[0x3ADDE]=(u8)i; called=0; func_8001F8B0_204B0(); assert(called==i+1); } puts("PASS USA dispatcher phases 0, 1, 2 (3/3)"); }
