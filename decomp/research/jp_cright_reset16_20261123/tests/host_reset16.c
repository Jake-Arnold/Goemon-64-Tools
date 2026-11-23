/* Synthetic-only host regression; no game ROM or proprietary data. */
#include <assert.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
typedef unsigned char u8;
u8 *g_system_ptr;
#include "../source/func_80004170_4D70.c"
#define OFFSET 0x3B168u
#define SPACE (OFFSET+16u*16u+64u)
static unsigned int step(unsigned int *x){*x^=*x<<13;*x^=*x>>17;*x^=*x<<5;return *x;}
int main(void){
    unsigned char *p=(unsigned char *)malloc(SPACE), *saved=(unsigned char *)malloc(SPACE);
    unsigned int i,j,seed=0x5CDAA4u;
    assert(p&&saved);
    g_system_ptr=p;
    for(j=0;j<128;j++){
        for(i=0;i<SPACE;i++)p[i]=(unsigned char)step(&seed);
        memcpy(saved,p,SPACE);
        func_80004170_4D70();
        for(i=0;i<SPACE;i++){
            const int target=(i>=OFFSET && i<OFFSET+16u*16u && (i-OFFSET)%16u==0);
            assert(p[i]==(target?0:saved[i]));
        }
    }
    free(saved);free(p);
    puts("128 synthetic reset16 full-buffer cases PASS");
    return 0;
}
