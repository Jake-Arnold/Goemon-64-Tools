/* Actual native-matching C body under host sanitizers, with bounded storage. */
#include <stdint.h>
#include <string.h>
#include <assert.h>
#include <stdio.h>
#include "../source/func_8000A5C4_B1C4.c"
A5C4Struct D_8005B974_5C574;
static uint32_t state=0xA5C4B1C4u;
static uint32_t next(void){state=state*1664525u+1013904223u;return state;}
int main(void) {
    A5C4Struct dest,expected;
    for (int test=0;test<4096;test++) {
        for(int i=0;i<38;i++) {
            D_8005B974_5C574.words[i]=next();
            dest.words[i]=next();
        }
        expected=D_8005B974_5C574;
        expected.words[0]=dest.words[0];
        func_8000A5C4_B1C4(&dest);
        assert(memcmp(&dest,&expected,sizeof dest)==0);
        /* Repeated call must still preserve the destination's old word zero. */
        D_8005B974_5C574.words[0]=next();
        func_8000A5C4_B1C4(&dest);
        assert(memcmp(&dest,&expected,sizeof dest)==0);
    }
    puts("PASS 4096 original-source copy-preserve trials, repeated call stable");
    return 0;
}
