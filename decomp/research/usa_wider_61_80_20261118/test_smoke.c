#include <assert.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>
static _Alignas(8) unsigned char actor[256];
static uint32_t get32(unsigned at){uint32_t x;memcpy(&x,actor+at,4);return x;}
static void put32(unsigned at,uint32_t x){memcpy(actor+at,&x,4);}
void func_0800033C_720C0C(void*,void*);
void func_08000C98_72A238(void);
int func_08000C88_72A228(void*);
void func_0800058C_72BDDC(void*,uint32_t);
int func_080005A8_72BDF8(void*);
void func_080014D0_72CD20(void*);
void func_080014DC_72CD2C(void*);
void func_08000CB8_733BE8(void*,uint32_t);
int func_08000DA8_733CD8(void*);
uint32_t func_080015B0_739C80(void*);
unsigned char func_080004A4_73CAB4(void*);
int main(void){
    func_0800033C_720C0C(actor,actor);
    func_08000C98_72A238();
    assert(func_08000C88_72A228(actor)==1);
    actor[0x74]=1;assert(func_08000C88_72A228(actor)==0);
    func_0800058C_72BDDC(actor,7);assert(get32(0x84)==210);
    func_0800058C_72BDDC(actor,0xFFFFFFFFu);assert(get32(0x84)==0xFFFFFFE2u);
    put32(0x84,(uint32_t)-95);assert(func_080005A8_72BDF8(actor)==-3);
    func_080014D0_72CD20(actor);assert(actor[0xD0]==255);
    func_080014DC_72CD2C(actor);assert(actor[0xD0]==254);
    func_08000CB8_733BE8(actor,0xABCDEF01u);assert(get32(0x60)==0xABCDEF01u);
    assert(func_08000DA8_733CD8(actor)==0);
    put32(0x6C,0xDEADBEEFu);assert(func_08000DA8_733CD8(actor)==1);
    put32(0x70,0x12345678u);assert(func_080015B0_739C80(actor)==0x12345678u);
    actor[0xD3]=0xA5;assert(func_080004A4_73CAB4(actor)==0xA5);
    puts("PASS resource61-80 exact-C smoke, ASan+UBSan");return 0;
}
