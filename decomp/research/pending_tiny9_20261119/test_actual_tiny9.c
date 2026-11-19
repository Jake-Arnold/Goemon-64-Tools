/* Execute the nine actual original-address C bodies using bounded host buffers. */
#include <stdint.h>
#include <stdio.h>
#include <string.h>
void func_801D36BC_5FEA9C(void *);
void func_801D36C4_5FEAA4(void *);
void func_801D3894_5FEC74(void *);
void func_801D389C_5FEC7C(void *);
void func_8021551C_6744CC(uint8_t *);
void func_802122CC_67BCAC(uint8_t *);
void func_0800185C_70929C(uint8_t *,int);
void func_0800142C_70B46C(uint8_t *);
void func_08001454_70B494(uint8_t *,int);

static int check(const uint8_t *got, size_t off, size_t width, int value) {
    size_t i;
    for (i=0; i<256; ++i)
        if (got[i]!=(i>=off && i<off+width ? (uint8_t)value : (uint8_t)0x5A)) return 0;
    return 1;
}
int main(void) {
    uint32_t buffer[64];
    uint8_t *p=(uint8_t *)buffer;
    int iteration;
    for (iteration=0;iteration<1000;iteration++) {
        memset(p,0x5A,256);func_801D36BC_5FEA9C(p);if(!check(p,0x34,4,0))return 1;
        memset(p,0x5A,256);func_801D36C4_5FEAA4(p);if(!check(p,0x34,4,0))return 2;
        memset(p,0x5A,256);func_801D3894_5FEC74(p);if(!check(p,0x38,4,0))return 3;
        memset(p,0x5A,256);func_801D389C_5FEC7C(p);if(!check(p,0x38,4,0))return 4;
        memset(p,0x5A,256);func_8021551C_6744CC(p);if(!check(p,0xA0,1,0))return 5;
        memset(p,0x5A,256);func_802122CC_67BCAC(p);if(!check(p,0x98,1,0))return 6;
        memset(p,0x5A,256);func_0800185C_70929C(p,iteration);if(!check(p,0xD1,1,iteration))return 7;
        memset(p,0x5A,256);func_0800142C_70B46C(p);if(!check(p,0xD0,1,0))return 8;
        memset(p,0x5A,256);func_08001454_70B494(p,iteration);if(!check(p,0xD2,1,iteration))return 9;
    }
    puts("PASS: 9 original-address C setters, 9000 ASan/UBSan host calls");
    return 0;
}
