#include <assert.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
struct ObjectNode {
  char pad_0[0x74];struct ObjectNode *child;
  char pad_78[0x1C];struct ObjectNode *next;
};
extern int func_80019160_19D60(struct ObjectNode *,void *);
static struct ObjectNode *expected_child, *expected_second_child, *mutate_owner, *replacement_next;
static void *expected_target;
static int calls, result_first, result_second;
int func_800191CC_19DCC(struct ObjectNode *child,void *target) {
 assert(target==expected_target);
 assert(child == (calls==0 ? expected_child : expected_second_child));
 if (mutate_owner) mutate_owner->next=replacement_next;
 return (calls++==0 ? result_first : result_second);
}
static void reset(void) {
 expected_child=expected_second_child=mutate_owner=replacement_next=0;
 expected_target=0;calls=0;result_first=result_second=0;
}
static void test_empty_and_last_node(void) {
 struct ObjectNode x={0}, y={0}, c={0};int marker=3;
 reset();expected_target=&marker;
 x.child=&c;
 assert(func_80019160_19D60(&x,&marker)==0);
 assert(calls==0); // no next => early exit, child not inspected
 expected_child=&c; x.next=&y;assert(func_80019160_19D60(&x,&marker)==0);
 assert(calls==1);
}
static void test_first_success_and_multi_hop(void) {
 struct ObjectNode a={0},b={0},c={0},child1={0},child2={0};int marker=77;
 reset();expected_target=&marker;
 a.next=&b;b.next=&c;a.child=&child1;b.child=&child2;
 expected_child=&child1;expected_second_child=&child2;
 result_first=1;
 assert(func_80019160_19D60(&a,&marker)==1);
 assert(calls==1);
 reset();expected_target=&marker;expected_child=&child1;expected_second_child=&child2;
 result_second=1;
 assert(func_80019160_19D60(&a,&marker)==1);
 assert(calls==2);
}
static void test_cached_next_ignores_callback_mutation(void) {
 struct ObjectNode a={0},b={0},c={0},other={0},child1={0},child2={0};int marker=42;
 reset();expected_target=&marker;
 a.next=&b;b.next=&c;a.child=&child1;b.child=&child2;
 expected_child=&child1;expected_second_child=&child2;result_second=1;
 mutate_owner=&a;replacement_next=&other;
 assert(func_80019160_19D60(&a,&marker)==1);
 assert(calls==2); // uses cached b, not modified a.next
}
int main(void) {
 /* Original N64 o32 uses four-byte pointers. Host 64-bit ABI differs. */
 if (sizeof(void*)==4) {
  assert(offsetof(struct ObjectNode,child)==0x74);
  assert(offsetof(struct ObjectNode,next)==0x94);
 }
 test_empty_and_last_node();test_first_success_and_multi_hop();test_cached_next_ignores_callback_mutation();
 puts("actor hierarchy traversal semantics: PASS");return 0;
}
