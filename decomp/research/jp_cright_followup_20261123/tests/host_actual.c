#include <assert.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "../sources/func_80212BD0_5CE160.c"
static unsigned char sysbuf[0x3B300];
unsigned char *g_system_ptr = sysbuf;
Stage D_80162420_163020;
u32 D_8020151C_5BD4EC, D_80201514_5BD4E4;
static unsigned count, calls, order[20];
static void *last_arg;
void func_8021E024_5D95B4(int x) { assert(x==10); ++count; }
void func_80212090_5CD620(void *arg) { ++calls; last_arg=arg; }
int func_800136A4_142A4(int arg) { assert(count<20); order[count++]=(unsigned)arg; return arg^0x315; }
void func_80004170_4D70(void);
void func_800041AC_4DAC(short slot);
int func_80013654_14254(unsigned short *list);
int main(void) {
    assert((uintptr_t)sysbuf<UINT32_MAX-0x3B300u);
    assert(offsetof(Stage,count)==0 && offsetof(Stage,present)==0x38 && offsetof(Stage,pending)==0xC4 && offsetof(Stage,previous)==0xC8 && offsetof(Stage,saved1)==0x12C && offsetof(Stage,saved2)==0x130);
    for(unsigned k=0;k<128;k++) {
        unsigned char initial=(unsigned char)(k+1);
        memset(sysbuf,initial,sizeof sysbuf);
        func_80004170_4D70();
        for(unsigned i=0;i<sizeof sysbuf;i++) assert(sysbuf[i]==((i>=0x3B168u && i<0x3B268u && (i-0x3B168u)%16==0)?0:initial));
        for(short i=0;i<16;i++) { memset(sysbuf+0x3B168,initial,256);func_800041AC_4DAC(i); for(unsigned j=0;j<256;j++)assert(sysbuf[0x3B168+j]==(j==(unsigned)i*16?0:initial)); }
        unsigned short ids[4]={(unsigned short)(k+1),(unsigned short)(65535-k),(unsigned short)(k+512),0}; count=0;
        assert(func_80013654_14254(ids)==(ids[2]^0x315));assert(count==3 && order[0]==ids[0] && order[1]==ids[1] && order[2]==ids[2]);
        memset(&D_80162420_163020,0,sizeof(Stage));D_80162420_163020.count=(u16)(65535u-k);D_80162420_163020.pending=k*1234u;D_80162420_163020.previous=0x11223344;D_80162420_163020.present=k&1;D_80162420_163020.saved1=77;D_80162420_163020.saved2=88;
        D_8020151C_5BD4EC=(k&2)?0x2345u+k:0;D_80201514_5BD4E4=0x3456u+k;count=calls=0;last_arg=0;
        func_80212BD0_5CE160(sysbuf,0);
        assert(D_80162420_163020.count==(u16)(65536u-k));assert(D_80162420_163020.previous==k*1234u && D_80162420_163020.pending==0);assert(count==1 && calls==(k&1));assert(!calls || last_arg==sysbuf);
        assert(D_80162420_163020.saved1==((k&2)?D_80201514_5BD4E4:77));assert(D_80162420_163020.saved2==((k&2)?D_8020151C_5BD4EC:88));
    }
    puts("PASS: 128 reset, 2048 indexed clear, 128 nonempty registration and 128 periodic cases");return 0;
}
