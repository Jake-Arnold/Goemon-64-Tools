/* Execute the actual native-matching C source with bounded host storage. */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "common.h"
#include "../sources/iso233_233.c"
#include "../sources/iso233_234.c"
#include "../sources/iso233_235.c"

SYS_W D_8008CCC0_8D8C0;
File92State D_8014CCC0_14D8C0;

static uint32_t rng=0xA18C0AAEu;
static u8 randbyte(void){rng=rng*1664525u+1013904223u;return (u8)(rng>>24);}

static u8 page[0x374*12+32];
static u8 expected_page[sizeof page];

int main(void){
    for(int test=0;test<4096;test++){
        for(size_t i=0;i<sizeof page;i++)page[i]=randbyte();
        memcpy(expected_page,page,sizeof page);
        for(int i=0;i<12;i++)expected_page[(i+1)*0x374-4]=0;
        func_8000AAE8_B6E8(page);
        assert(memcmp(page,expected_page,sizeof page)==0);

        memset(&D_8008CCC0_8D8C0,randbyte(),sizeof D_8008CCC0_8D8C0);
        SYS_W expected_sys=D_8008CCC0_8D8C0;
        for(int i=0;i<12;i++)expected_sys.bytes[0xC0000+i*0x374+0x3705]=0;
        func_8000AB30_B730();
        assert(memcmp(&D_8008CCC0_8D8C0,&expected_sys,sizeof expected_sys)==0);

        memset(&D_8014CCC0_14D8C0,randbyte(),sizeof D_8014CCC0_14D8C0);
        File92State expected_state=D_8014CCC0_14D8C0;
        expected_state.field_5D06=255;
        expected_state.field_5D08=255;
        expected_state.field_5D0A=255;
        expected_state.field_5D0C=255;
        expected_state.field_5D10=0;
        func_8000A18C_AD8C();
        assert(memcmp(&D_8014CCC0_14D8C0,&expected_state,sizeof expected_state)==0);
    }
    puts("PASS: 4096 actual-source cases per A18C, AAE8 and AB30");
    return 0;
}
