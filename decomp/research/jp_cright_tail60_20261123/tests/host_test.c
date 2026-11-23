#include <assert.h>
#include <stddef.h>

typedef unsigned char u8;
u8 g_system[32];
u8 *g_system_ptr;
static int order;

void func_80004170_4D70(void){ assert(g_system_ptr == g_system);assert(order == 0);order=1; }
void func_8000339C_3F9C(void){ assert(g_system_ptr == g_system);assert(order == 1);order=2; }
void func_80212C50_5CE1E0(void*,void*);
int main(void){
  u8 other[64];
  for(int i=0;i<64;i++){
    g_system_ptr=other;
    order=0;
    func_80212C50_5CE1E0((void*)(size_t)(0x1000+i),(void*)(size_t)(0x2000+i));
    assert(g_system_ptr==g_system);
    assert(order==2);
  }
  return 0;
}
