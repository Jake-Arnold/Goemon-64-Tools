/* Actual native-source behavioural fixtures: 4096 cases per build. */
#ifdef JAPAN
#include "sources/func_8021BB8C_5D711C_basic.c"
#define VALUE D_8023F220_5FA7B0
#define CALLBACK func_8021BA50_5D6FE0
#define TARGET func_8021BB8C_5D711C
#else
#include "sources/func_80216E1C_5D22EC_basic.c"
#define VALUE D_8023A510_5F59E0
#define CALLBACK func_80216CE0_5D21B0
#define TARGET func_80216E1C_5D22EC
#endif
float VALUE;
static Task task;
static Obj child;
static int call_count, errors, expected_kind;
static unsigned long cases;
static float expected_value;
#define CHECK(c) do { if(!(c))++errors; } while(0)
void CALLBACK(Task *a,Obj *b,int kind) {
  call_count++;
  CHECK(a==&task && b==&child && kind==expected_kind);
  CHECK(b->x==expected_value && b->y==expected_value && b->z==expected_value);
  b->x=123.0f; /* Verify callback occurs AFTER all three assignments. */
}
int main(void){
  unsigned i; union { unsigned u; float f; } v;
  task.child=&child;
  for(i=0;i<4096;i++) {
    v.u=0x3F000000u+((i*217u)&0x007fffffu);
    VALUE=v.f;expected_value=v.f;expected_kind=(int)(i*31u)-13000;
    child.x=-999.0f;child.y=-998.0f;child.z=-997.0f;
    TARGET(&task,expected_kind);
    CHECK(call_count==(int)i+1);
    CHECK(child.x==123.0f && child.y==v.f && child.z==v.f);
    cases++;
  }
  return errors || call_count!=4096 || cases!=4096;
}
