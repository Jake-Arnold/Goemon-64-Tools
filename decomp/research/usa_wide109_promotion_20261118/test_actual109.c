/* Host regressions for exact source bodies from USA wide109, not native proof. */
#include <assert.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include <stdalign.h>
#include <stddef.h>
extern signed char func_080009DC_70AA1C(unsigned char *);
extern void func_80210618_698018(unsigned char*,unsigned short);
extern void func_80210C78_698678(unsigned char*,unsigned short);
extern unsigned short func_802143D0_69BDD0(unsigned char *);
extern void func_80211694_699094(unsigned char*,float);
extern void func_802196E4_5D4BB4(unsigned char*);
extern void func_08000F70_72A510(unsigned char*,float);
extern void func_80213ED0_5CF3A0(void*,void*);
extern void func_80213EDC_5CF3AC(void*,void*);
int main(void) {
    union {max_align_t alignment; unsigned char memory[512];} buf;
    unsigned char baseline[512];
    for (unsigned i=0;i<1000;i++) {
        memset(buf.memory,0xA5,sizeof buf.memory);
        func_80210618_698018(buf.memory,(unsigned short)(0x1000+i));
        func_80210C78_698678(buf.memory,(unsigned short)(0xB000+i));
        assert(*(unsigned short*)(buf.memory+152)==(unsigned short)(0x1000+i));
        assert(func_802143D0_69BDD0(buf.memory)==(unsigned short)(0xB000+i));
        assert(buf.memory[151]==0xA5 && buf.memory[154]==0xA5 && buf.memory[114]==0xA5 && buf.memory[118]==0xA5);
        func_80211694_699094(buf.memory,(float)i/7.0f);
        func_08000F70_72A510(buf.memory,(float)i/13.0f);
        assert(*(float*)(buf.memory+92)==(float)i/7.0f);
        assert(*(float*)(buf.memory+236)==(float)i/13.0f);
        *(signed char*)(buf.memory+209)=(signed char)(i-120);
        assert(func_080009DC_70AA1C(buf.memory)==(signed char)(i-120));
        *(float*)(buf.memory+120)=1.0f;
        *(float*)(buf.memory+124)=2.0f;
        *(float*)(buf.memory+128)=3.0f;
        func_802196E4_5D4BB4(buf.memory);
        assert(*(float*)(buf.memory+120)==0.0f && *(float*)(buf.memory+124)==0.0f && *(float*)(buf.memory+128)==0.0f);
        memcpy(baseline,buf.memory,sizeof baseline);
        func_80213ED0_5CF3A0(buf.memory,buf.memory+32);
        func_80213EDC_5CF3AC(buf.memory,buf.memory+32);
        assert(memcmp(baseline,buf.memory,sizeof baseline)==0);
    }
    puts("PASS: 1000 wide109 actual-source setter/getter/no-op regression iterations");
    return 0;
}
