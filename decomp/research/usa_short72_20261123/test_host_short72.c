/* Host ASan/UBSan runs the exact two original native C timer sources. */
#include <stdint.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
struct A { unsigned char pad[0xD4]; int32_t timer; };
extern void func_801F1B78_61CF58(struct A*);
extern void func_801F1BA8_61CF88(struct A*);
static unsigned calls_a,calls_b;
static void *ptr_a,*ptr_b;
void func_801F1D78_61D158(void *p){calls_a++;ptr_a=p;}
void func_801F1E94_61D274(void *p){calls_b++;ptr_b=p;}
int main(void){
    struct A a,b;
    for (int i=-1023;i<=3072;i++) {
        memset(&a,0,sizeof(a));memset(&b,0,sizeof(b));
        a.timer=i;b.timer=i;
        unsigned ca=calls_a,cb=calls_b;
        func_801F1B78_61CF58(&a);
        func_801F1BA8_61CF88(&b);
        if (a.timer!=i-1 || b.timer!=i-1 ||
            calls_a!=ca+(i<=1) || calls_b!=cb+(i<=1) ||
            (i<=1 && (ptr_a!=&a || ptr_b!=&b))) {
            fprintf(stderr,"Original C timer semantics mismatch at %d\n",i);return 1;
        }
    }
    if (calls_a!=1025 || calls_b!=1025) return 2;
    puts("PASS 4096 input pairs, actual original 48B timer sources, both callbacks and boundary controls");
    return 0;
}
