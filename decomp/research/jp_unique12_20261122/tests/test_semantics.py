#!/usr/bin/env python3
"""Compile *actual* reconstructed source under GCC ASan/UBSan and run host fixtures.

No claim of executing original MIPS or validating 32 MiB native build.
The pointer-as-symbolic-offset candidate is native-verified but only host-compiled:
its original MIPS32 address model cannot be safely represented as a host pointer.
"""
from pathlib import Path
import argparse, subprocess, tempfile, os

root=Path(__file__).resolve().parents[1]
# Fixtures include the actual candidate source directly, so no fake/mocked implementation.
# Each is a separate translation unit to avoid name/type collisions between unrelated structs.
fixtures={
'func_801EF790_61A210':r'''
char *D_80214600_63F080;
int main(void){unsigned int data[160];for(int i=0;i<160;i++)data[i]=0x55667788;
 D_80214600_63F080=(char*)data;func_801EF790_61A210();
 assert(data[0x174/4]==0);assert(data[0x170/4]==0x55667788);assert(data[0x178/4]==0x55667788);return 0;}
''',
'func_801E818C_5A415C':r'''
static int calls;void func_801E815C_5A412C(void){calls++;}
int main(void){for(int i=0;i<2048;i++)func_801E818C_5A415C();assert(calls==2048);return 0;}
''',
'func_801E83A0_5A4370':r'''
int main(void){for(int j=0;j<256;j++){T p={{0}};p.b[0x30]=(unsigned char)j;
 func_801E83A0_5A4370(&p);assert(p.b[0xD4]==60);assert(p.b[0x30]==((j&~1)|4));}
 return 0;}
''',
'func_8021B3F8_67A268':r'''
unsigned char D_8021BEA0_67AD10[120*2048+64];
int main(void){for(int i=0;i<2048;i++){unsigned char *p=func_8021B3F8_67A268(i);
 assert(p==D_8021BEA0_67AD10+i*120+2);}return 0;}
''',
'func_8021251C_67BC0C':r'''
/* Compile-time check only: no host execution of 32-bit address-valued symbol D_CF8FC. */
char *g_system_ptr;
char D_CF8FC;
int main(void){return 0;}
''',
'func_8021BB68_5D70F8':r'''
static struct X *got_p;static void *got_q;static int got_n,calls;
void func_8021BA50_5D6FE0(struct X*p,void*q,int n){got_p=p;got_q=q;got_n=n;calls++;}
int main(void){struct X x={{0},0};int value=42;x.p=&value;
for(int i=0;i<2048;i++){func_8021BB68_5D70F8(&x,i);assert(got_p==&x&&got_q==&value&&got_n==i);}
assert(calls==2048);return 0;}
''',
'func_801EC4E8_5A84B8':r'''
int main(void){for(int x=0;x<256;x++)for(int y=0;y<256;y++){
struct X p={{0},(unsigned char)x};func_801EC4E8_5A84B8(&p,(unsigned char)y);
assert(p.val==(x>y?x:y));}return 0;}
''',
'func_80200DAC_62B82C':r'''
static void *got_p,*got_q;static int calls;
void func_80201B2C_62C5AC(void*p,void*q){got_p=p;got_q=q;calls++;}
int main(void){unsigned char src[32]={0};int tag=42;for(int i=0;i<2048;i++){
src[5]=0;func_80200DAC_62B82C(&tag,(char*)src);assert(src[5]==5&&got_p==&tag&&got_q==src);}
assert(calls==2048);return 0;}
''',
'func_801F9560_5B5530':r'''
static void*got;static int a,b,calls;
void func_801F9B78_5B5B48(void*p,int x,int y){got=p;a=x;b=y;calls++;}
int main(void){int obj;for(int i=0;i<2048;i++){func_801F9560_5B5530(&obj,(void*)(unsigned long)i);
assert(got==&obj&&a==0&&b==0);}assert(calls==2048);return 0;}
''',
'func_801E60F0_5A20C0':r'''
static void*got;static int a,b,calls;
void func_801ECC4C_5A8C1C(void*p,int x,int y){got=p;a=x;b=y;calls++;}
int main(void){int obj;for(int i=0;i<2048;i++){func_801E60F0_5A20C0(&obj,(void*)(unsigned long)i);
assert(got==&obj&&a==0&&b==0);}assert(calls==2048);return 0;}
''',
'func_801E6118_5A20E8':r'''
static void*got;static int a,b,calls;
void func_801ECC4C_5A8C1C(void*p,int x,int y){got=p;a=x;b=y;calls++;}
int main(void){int obj;for(int i=0;i<2048;i++){func_801E6118_5A20E8(&obj,(void*)(unsigned long)i);
assert(got==&obj&&a==1&&b==0);}assert(calls==2048);return 0;}
''',
'func_8021B3D0_67A240':r'''
char D_8021BEA0_67AD10[120*16+16*16+64];
int main(void){for(int i=0;i<16;i++)for(int j=0;j<16;j++){
char*p=func_8021B3D0_67A240(i,j);
assert(p==D_8021BEA0_67AD10+i*120+j*16+0x20);}return 0;}
''',
}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--cc',default='gcc');args=ap.parse_args()
    with tempfile.TemporaryDirectory(prefix='jp-unique12-host-') as td:
        td=Path(td)
        for name,fixture in fixtures.items():
            src=(root/'sources'/(name+'.c')).resolve()
            code='#include <assert.h>\n#include <stdint.h>\n#include <stddef.h>\n#include "'+str(src)+'"\n'+fixture
            c=td/(name+'.c');exe=td/name;c.write_text(code)
            cmd=[args.cc,'-std=gnu11','-O1','-g','-fno-omit-frame-pointer','-fsanitize=address,undefined','-o',exe,c]
            p=subprocess.run(cmd,capture_output=True,text=True)
            if p.returncode:raise RuntimeError(f'{name} HOST COMPILE FAILED {p.stderr}')
            env=os.environ.copy();env['ASAN_OPTIONS']='detect_leaks=1:abort_on_error=1'
            # ASan runtime startup can be flaky in some containers; error remains a failure.
            p=subprocess.run([str(exe)],capture_output=True,text=True,env=env)
            if p.returncode:raise RuntimeError(f'{name} HOST RUN FAILED {p.returncode} {p.stderr[-1400:]}')
            print(f'HOST ASAN UBSAN PASS {name} '+('COMPILE_ONLY' if name=='func_8021251C_67BC0C' else 'EXECUTED'))
    print('PASS: 12 actual C implementations compiled under sanitizers; 11 semantic fixtures executed; one pointer-valued symbol candidate compiled only.')
if __name__=='__main__':main()
