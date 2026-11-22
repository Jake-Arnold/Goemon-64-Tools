/* Test the actual IDO-matching C sources; all guest addresses are replaced by bounded host storage. */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "../source/func_8000A18C_AD8C.c"
#include "../source/func_800108BC_114BC.c"

char D_800637C0_643C0[32];
SYS_W D_8008CCC0_8D8C0;
File92State D_8014CCC0_14D8C0;
void func_8000AAE8_B6E8(u8 *p);
void func_8000AB30_B730(void);

static uint32_t rng=0x1924EFA3u;
static uint8_t randbyte(void){rng=rng*1664525u+1013904223u;return (uint8_t)(rng>>24);}
static u8 page[0x374*12+32];
static u8 expected_page[sizeof page];
static SYS_W expected_sys;
static File92State expected_state;

int main(void){
  for(int test=0;test<4096;test++){
    memset(page,randbyte(),sizeof page);
    memcpy(expected_page,page,sizeof page);
    for (int i=0;i<12;i++) expected_page[(i+1)*0x374-4]=0;
    func_8000AAE8_B6E8(page);
    assert(memcmp(page,expected_page,sizeof page)==0);

    memset(D_8008CCC0_8D8C0.bytes,randbyte(),sizeof D_8008CCC0_8D8C0.bytes);
    expected_sys=D_8008CCC0_8D8C0;
    for (int i=0;i<12;i++) expected_sys.bytes[0xC0000 + i*0x374 + 0x3705]=0;
    func_8000AB30_B730();
    assert(memcmp(&D_8008CCC0_8D8C0,&expected_sys,sizeof expected_sys)==0);

    memset(&D_8014CCC0_14D8C0,randbyte(),sizeof D_8014CCC0_14D8C0);
    expected_state=D_8014CCC0_14D8C0;
    expected_state.field_5D06=255;
    expected_state.field_5D08=255;
    expected_state.field_5D0A=255;
    expected_state.field_5D0C=255;
    expected_state.field_5D10=0;
    func_8000A18C_AD8C();
    assert(memcmp(&D_8014CCC0_14D8C0,&expected_state,sizeof expected_state)==0);

    /* Full contents, return-value and untouched-neighbour validation of
       the original two-command display-list wrapper. */
    RawGfx gfx[16], want[16];
    for (size_t k=0;k<16;k++) { gfx[k].w0=(uint32_t)rng; rng=rng*1664525u+1013904223u;
                                  gfx[k].w1=(uint32_t)rng; rng=rng*1664525u+1013904223u; }
    memcpy(want,gfx,sizeof gfx);
    size_t index=1+((unsigned)test%13);
    want[index].w0=0x06000000u;
    want[index].w1=(uint32_t)(uintptr_t)D_800637C0_643C0;
    want[index+1].w0=0xB8000000u;
    want[index+1].w1=0;
    RawGfx *end = func_800108BC_114BC(gfx+index);
    assert(end == gfx+index+1);
    assert(memcmp(gfx,want,sizeof gfx)==0);

  }
  puts("PASS: 4096 cases per source across four original-USA C implementations");
  return 0;
}
