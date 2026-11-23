#include <assert.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
typedef unsigned char u8;
typedef unsigned short u16;
u8 *D_8015C5C8_15D1C8;
u16 D_8022A380_693D60[8];
static u16 observed_event;
static unsigned events;
void func_80013B14_14714(u16 n) { observed_event = n; events++; }
void func_8020D7E8_6771C8(void);
void func_8021F330_688D10(int);
static uint32_t seed = 0x4202026;
static uint32_t rng(void){uint32_t x=seed;x^=x<<13;x^=x>>17;x^=x<<5;return seed=x;}
int main(void) {
  // Original N64 symbolic offset D_CF8F8 is represented by absolute linker symbol.
  D_8015C5C8_15D1C8=calloc(1,0xD0000);
  if(!D_8015C5C8_15D1C8)return 3;
  u8 parent[0x100]={0},child[0x100]={0};
  for(int i=0;i<10000;i++) {
    u8 *target=parent;
    memcpy(D_8015C5C8_15D1C8+0xCF8F8,&target,sizeof(target));
    parent[0x64]=0xFF;child[0x64]=0xFF;
    u8 *dependent=(i%3 ? child : NULL);
    memcpy(parent,&dependent,sizeof(dependent));
    func_8020D7E8_6771C8();
    assert(parent[0x64]==0);
    assert(child[0x64]==(dependent ? 0 : 0xFF));
    for(int j=0;j<8;j++)D_8022A380_693D60[j]=(u16)rng();
    int index=(int)(rng()%8);unsigned before=events;
    func_8021F330_688D10(index);
    assert(events==before+1);
    assert(observed_event==D_8022A380_693D60[index]);
  }
  free(D_8015C5C8_15D1C8);
  puts("PASS: 10,000 callback/flag/selector cases with ASan+UBSan");
  return 0;
}
