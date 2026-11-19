"""New original-C micro20 source fingerprint and host semantic tests; not native ROM proof."""
import hashlib
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from decomp import overlay_micro20


class Micro20Tests(unittest.TestCase):
    def test_pinned_sources(self):
        j = overlay_micro20.load_fixture()
        self.assertEqual(len(j['units']), 20)
        self.assertEqual(len(overlay_micro20.functions(j)), 20)
        self.assertEqual(sum(f['size'] for f in overlay_micro20.functions(j)), 368)
        for u in j['units']:
            data = (overlay_micro20.SOURCE_BASE / (u['name'] + '.c')).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), u['source_sha256'])

    @unittest.skipUnless(shutil.which('gcc'), 'GCC required for original source ASan/UBSan test')
    def test_actual_native_sources_with_sanitizers(self):
        fixture=overlay_micro20.load_fixture()
        sources = [str(overlay_micro20.SOURCE_BASE / (u['name']+'.c')) for u in fixture['units']]
        harness = r'''
#include <assert.h>
#include <stdint.h>
#include <string.h>
#include <limits.h>
void func_8021B034_5D6504(char *,int);
void func_801D609C_60147C(char *);
void func_801D60B4_601494(char *);
void func_801D60CC_6014AC(char *);
void func_801E3600_60E9E0(void *,char *);
void func_80214E98_673E48(char *);
void func_80214EA8_673E58(char *);
void func_8021B120_684B00(char *,int);
float func_8021C844_686224(int *);
void func_80224418_68DDF8(char *,float,float,int);
void func_8022472C_68E10C(char *,float,float,int);
void *func_80226514_68FEF4(char *,int);
void *func_80210638_698038(char *,float);
void *func_802108EC_6982EC(char *,float);
void *func_80212B30_69A530(char *,float);
void func_8021306C_69AA6C(char *,int);
void func_8021451C_69BF1C(char *,int);
void func_08003A74_6C31C4(char *,int);
int func_08001380_730C10(unsigned int *);
int func_080012FC_73422C(unsigned int *);
static union {uint64_t align; unsigned char data[512];} state,target,third;
int main(void){
    unsigned char *p=state.data,*q=target.data,*r=third.data;
    /* Native pointers in the N64 fields are 32-bit. Host fixture's globals
       reside below 4GiB under -no-pie, preserving the test's pointer width. */
    assert((uintptr_t)q<=UINT32_MAX && (uintptr_t)r<=UINT32_MAX);
    for(int i=0;i<1000;i++){
        memset(p,0,512);memset(q,0,512);memset(r,0,512);
        func_8021B034_5D6504((char*)p,i);assert(*(short *)(p+0x8A)==(short)i);
        assert(*(float *)(p+0xD0)==0 && *(float *)(p+0xD4)==0 && *(float *)(p+0xD8)==0);
        *(uint32_t *)(p+24)=(uint32_t)(uintptr_t)q;
        *(float *)(p+0x70)=0.25f;*(float *)(p+0x74)=0.5f;*(float *)(p+0x78)=0.75f;
        *(float *)(q+8)=1.f;*(float *)(q+12)=2.f;*(float *)(q+16)=3.f;
        func_801D609C_60147C((char*)p);func_801D60B4_601494((char*)p);func_801D60CC_6014AC((char*)p);
        assert(*(float *)(q+8)==1.25f && *(float *)(q+12)==2.5f && *(float *)(q+16)==3.75f);
        *(float *)(q+0x14)=5.5f;*(float *)(q+0x18)=2.5f;
        func_801E3600_60E9E0(p,(char*)q);
        assert(*(float *)(q+0x14)==0 && *(float *)(q+0x18)==0);
        func_80214E98_673E48((char*)p);assert(*(float *)(p+0xA4)==87.5f);
        func_80214EA8_673E58((char*)p);assert(*(float *)(p+0xA4)==-112.5f);
        *(uint32_t *)(p+0xB4)=(uint32_t)(uintptr_t)q;
        *(uint32_t *)(p+0xB0)=(uint32_t)(uintptr_t)r;
        func_8021B120_684B00((char*)p,i);assert(q[5]==(unsigned char)i && r[5]==(unsigned char)i);
        *(float *)(q+0x24)=(float)i*0.25f;
        assert(func_8021C844_686224((int *)p)==(float)i*0.25f);
        func_80224418_68DDF8((char*)p,5.25f,6.5f,i);
        assert(*(short *)(p+0x5E)==(short)i && *(float *)(p+0x68)==5.25f && *(float *)(p+0x74)==6.5f);
        func_8022472C_68E10C((char*)p,2.5f,3.25f,i);
        assert(*(short *)(p+0x5E)==(short)i && *(float *)(p+0x68)==2.5f && *(float *)(p+0x74)==3.25f);
        assert(func_80226514_68FEF4((char*)p,i)==q && q[5]==(unsigned char)i);
        assert(func_80210638_698038((char*)p,1.5f)==q && *(float *)(q+40)==1.5f);
        assert(func_802108EC_6982EC((char*)p,2.5f)==q && *(float *)(q+40)==2.5f);
        void *qptr=q; memcpy(p+0x5c,&qptr,sizeof(qptr));
        assert(func_80212B30_69A530((char*)p,3.5f)==q && *(float *)(q+8)==3.5f);
        *(uint32_t *)(p+0x88)=(uint32_t)(uintptr_t)q;
        func_8021306C_69AA6C((char*)p,i);assert(*(short *)(q+12)==(short)i);
        func_8021451C_69BF1C((char*)p,i);
        assert(*(uint32_t *)(q+0x2C)==(uint32_t)(i+0x40000000));
        *(float *)(p+0x78)=10;*(float *)(p+0x7c)=20;*(float *)(p+0x80)=30;
        func_08003A74_6C31C4((char*)p,i);
        assert(*(float *)(p+0x78)==0 && *(float *)(p+0x7c)==0 && *(float *)(p+0x80)==0);
        ((uint32_t *)p)[0xD0/4]=(uint32_t)(uintptr_t)q;
        ((uint32_t *)q)[4]=i;
        assert(func_08001380_730C10((uint32_t *)p)==i);
        assert(func_080012FC_73422C((uint32_t *)p)==i);
    }
    return 0;
}
'''
        with tempfile.TemporaryDirectory() as d:
            c=Path(d)/'host.c';exe=Path(d)/'host'
            c.write_text(harness)
            # The N64 field at 0x5c contains a 4-byte pointer, aligned to 4.
            # On x86-64 it is an 8-byte host pointer at offset 4 modulo 8.
            # Disable only host alignment UBSan for this one original source;
            # preserve its ASan and other UBSan checks and all other source checks.
            special = next(x for x in sources if x.endswith('micro20_014.c'))
            other_sources = [x for x in sources if x != special]
            special_object = Path(d) / 'n64-pointer-abi.o'
            common = ['-std=c99','-O1','-g','-fno-pie','-no-pie',
                      '-fsanitize=address,undefined','-fno-omit-frame-pointer',
                      '-Wno-int-to-pointer-cast','-Wno-pointer-to-int-cast']
            isolated = subprocess.run(['gcc',*common,'-fno-sanitize=alignment',
                 '-c','-o',str(special_object),special],capture_output=True,text=True)
            self.assertEqual(isolated.returncode,0,isolated.stderr)
            build=subprocess.run(['gcc',*common,
                '-o',str(exe),*other_sources,str(special_object),str(c)],
                capture_output=True,text=True)
            self.assertEqual(build.returncode,0,build.stderr)
            run=subprocess.run([str(exe)],capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stderr)

if __name__=='__main__':unittest.main()
