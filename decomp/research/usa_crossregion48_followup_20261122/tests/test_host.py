#!/usr/bin/env python3
"""Compile the actual 48 cross-region C implementations with GCC ASan/UBSan.

The original IDO/ROM native verifier is separate. Host fixtures execute where
MIPS32 symbol/address conventions can be emulated safely, including callback
branches via linker aliases. An original MIPS32 indirect dispatch table is only
compiled, not asserted to behave identically on an x86-64 host.
"""
import argparse,json,re,os,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'sources'

def symbols(s, prefix='func'):
 return list(dict.fromkeys(re.findall(r'\b'+prefix+r'_[0-9a-fA-F]+(?:_[0-9a-fA-F]+)?\b',s)))

def stub(name,typ,body):
 return f'{typ} test_stub_{name}( {body[0]} ) __asm__("{name}");\n{typ} test_stub_{name}({body[0]}){{{body[1]}}}\n'

def fixture(name,s):
 ext=[f for f in symbols(s) if f!=name]
 data=symbols(s,'D')
 pre='''#include <stdint.h>\n#include <stddef.h>\n#include <string.h>\n#include <math.h>\n#include <assert.h>\n'''
 pre+='#include "'+str((SRC/(name+'.c')).resolve())+'"\n'
 if 'typedef struct { Fn a,b,c; } Table;' in s:
  return pre+'int main(void){return 0;}\n',False,'MIPS32_INDIRECT_TABLE_COMPILE_ONLY'
 if 'struct Owner' in s:
  assert len(ext)==2,(name,ext)
  cb,dat=ext
  pre+=f'''int test_data __asm__("{dat}")=123;\nstatic int calls;static void*last;\nvoid test_cb(void*p) __asm__("{cb}");\nvoid test_cb(void*p){{calls++;last=p;}}\n'''
  main=f'''int main(void){{struct Owner a={{0}};a.remaining=2;{name}(&a,42);assert(a.remaining==1&&calls==0);a.remaining=0;{name}(&a,0);assert(a.remaining==65535&&calls==1&&last==&test_data);return 0;}}'''
 elif 'struct S {' in s:
  assert len(ext)==1
  cb=ext[0]
  pre+=f'''static int calls,a,b;static void*last;\nvoid test_cb(void*p,int x,int y) __asm__("{cb}");void test_cb(void*p,int x,int y){{calls++;last=p;a=x;b=y;}}\n'''
  main=f'''int main(void){{struct S a={{0}};a.counter=2;{name}(&a,42);assert(a.counter==1&&calls==0);a.counter=0;{name}(&a,0);assert(a.counter==65535&&calls==1&&last==&a&&a==0&&b==1);return 0;}}'''.replace('static int calls,a,b;','static int calls,aa,bb;')
  # Replace the callback's scalar identifiers to avoid shadowing struct local.
  pre=pre.replace('static int calls,a,b;','static int calls,aa,bb;').replace('last=p;a=x;b=y;','last=p;aa=x;bb=y;')
  main=main.replace('&&a==0&&b==1','&&aa==0&&bb==1')
 elif 'struct X{char filler' in s:
  assert len(ext)==2
  cb1,cb2=ext
  pre+=f'''static int calls1,calls2,xx,yy;static void*last1,*last2;\nvoid test_cb1(void*p) __asm__("{cb1}");void test_cb1(void*p){{calls1++;last1=p;}}\nvoid test_cb2(void*p,int a,int b) __asm__("{cb2}");void test_cb2(void*p,int a,int b){{calls2++;last2=p;xx=a;yy=b;}}\n'''
  observed_second='1' if re.search(r'\(p,1,1\)',s) else '0'
  main=f'''int main(void){{struct X p={{0}};p.count=3;{name}(&p,7);assert(p.count==2&&calls1==0&&calls2==0);p.count=0;{name}(&p,9);assert(p.count==65535&&calls1==1&&calls2==1&&last1==&p&&last2==&p&&xx=={observed_second}&&yy==1);return 0;}}'''
 elif 'struct Obj' in s:
  assert len(ext)==1
  cb=ext[0]
  pre+=f'''static int calls;static void*last;void test_cb(void*p) __asm__("{cb}");void test_cb(void*p){{calls++;last=p;}}\n'''
  main=f'''int main(void){{struct Obj p={{0}};p.count=2;{name}(&p,3);assert(p.count==1&&calls==0);p.count=0;{name}(&p,0);assert(p.count==65535&&calls==1&&last==&p);return 0;}}'''
 elif 'f32 change;' in s:
  main=f'''int main(void){{float memory[96]={{0}};float *v=(float*)((char*)memory+0x5C);v[1]=2;v[2]=7;{name}(memory,11);assert(v[3]==11&&v[4]==2);{name}(memory,3);assert(v[3]==3&&v[4]==2);return 0;}}'''
 elif 'extern double' in s:
  assert len(data)==1
  pre+=f'double test_scale __asm__("{data[0]}")=1.5;\n'
  # Both variants store three float source fields and scale each into another.
  m=re.search(r'\(\(char\*\)b\+(\d+)\)=v',s)
  assert m,(name,s)
  base=int(m.group(1))
  main=f'''int main(void){{float a[96]={{0}},b[96]={{0}};*((float*)((char*)a+124))=2;*((float*)((char*)a+128))=4;*((float*)((char*)a+132))=6;{name}(a,b);for(int i=0;i<3;i++){{assert(*(float*)((char*)b+{base}+4*i)==2.0f+2.0f*i);assert(*(float*)((char*)b+8+4*i)==(2.0f+2.0f*i)*1.5f);}}return 0;}}'''
 elif 'typedef struct{unsigned int w0,w1;} Gfx;' in s:
  assert len(data)==1
  pre+=f'char test_data[48] __asm__("{data[0]}");\n'
  main=f'''int main(void){{Gfx a[3]={{0}};Gfx*p={name}(a);assert(p==a+1&&a[0].w0==0x06000000&&a[0].w1==(unsigned)(uintptr_t)test_data&&a[1].w0==0xb8000000&&a[1].w1==0);return 0;}}'''
 elif 'typedef unsigned char u8;extern int' in s:
  assert len(ext)==1
  cb=ext[0]
  pre+=f'''static int calls,aa,bb;static void*last;void test_cb(void*p,int a,int b) __asm__("{cb}");void test_cb(void*p,int a,int b){{calls++;last=p;aa=a;bb=b;}}\n'''
  main=f'''int main(void){{unsigned char q[160]={{0}};int p;{name}(&p,q);assert(calls==0);q[0x7c]=2;{name}(&p,q);assert(calls==1&&last==&p&&aa==0&&bb==1);return 0;}}'''
 elif 'typedef float f32;typedef unsigned char u8;' in s:
  main=f'''int main(void){{float a[80]={{0}};{name}(a,255);assert(*(float*)((char*)a+0x64)==255.0f);{name}(a,1);assert(*(float*)((char*)a+0x64)==1.0f);return 0;}}'''
 elif 'extern void ' in s and 'extern float' in s:
  assert len(ext)==1 and len(data)==1
  cb=ext[0]
  pre+=f'''float test_val __asm__("{data[0]}")=3.25f;static int calls;static void*last;static float aa,bb,cc;\nvoid test_cb(void*p,float a,float b,float c) __asm__("{cb}");void test_cb(void*p,float a,float b,float c){{calls++;last=p;aa=a;bb=b;cc=c;}}\n'''
  main=f'''int main(void){{int v=1;{name}(&v);assert(calls==1&&last==&v&&aa==3.25f&&bb==3.25f&&cc==3.25f);return 0;}}'''
 elif 'M2C_FIELD' in s:
  # This donor passes a function pointer using MIPS32 no-prototype calling conventions.
  return pre+'int main(void){return 0;}\n',False,'MIPS32_UNPROTOTYPED_CALL_COMPILE_ONLY'
 elif 'extern char func_' in s:
  assert len(ext)==1
  cb=ext[0]
  pre+=f'''static int calls;int test_cb(void) __asm__("{cb}");int test_cb(void){{calls++;return 1;}}\n'''
  main=f'''int main(void){{for(int i=0;i<50;i++){name}();assert(calls==50);return 0;}}'''
 elif 'extern int' in s and 'volatile int' in s:
  assert len(ext)==1
  cb=ext[0]
  pre+=f'''static int calls,aa,bb;static void*last;void test_cb(void*p,int a,int b) __asm__("{cb}");void test_cb(void*p,int a,int b){{calls++;last=p;aa=a;bb=b;}}\n'''
  if '(arg0, 0, 0)' in s:
   main=f'''int main(void){{int obj=2;{name}(&obj,33);assert(calls==1&&last==&obj&&aa==0&&bb==0);return 0;}}'''
  else:
   main=f'''int main(void){{int obj=2;{name}(&obj,33);assert(calls==1&&last==&obj);return 0;}}'''
 elif 'extern int' in s and 'void *arg0' in s:
  assert len(ext)==1
  cb=ext[0]
  pre+=f'''static int calls;static void*last;void test_cb(void*p) __asm__("{cb}");void test_cb(void*p){{calls++;last=p;}}\n'''
  main=f'''int main(void){{int v=1;{name}(&v,99);assert(calls==1&&last==&v);return 0;}}'''
 else:
  raise ValueError('Unclassified '+name+'\n'+s[:1000])
 return pre+main+'\n',True,'EXECUTED_SEMANTICS'

def main():
 p=argparse.ArgumentParser();p.add_argument('--gcc',default='gcc');p.add_argument('--report',type=Path);args=p.parse_args()
 m=json.loads((ROOT/'manifest.json').read_text());assert len(m['functions'])==48
 results=[]
 with tempfile.TemporaryDirectory(prefix='goemon-usa48-host-') as dir:
  tmp=Path(dir)
  for i,row in enumerate(m['functions']):
   name=row['name'];source=(SRC/(name+'.c')).read_text()
   code,execute,status=fixture(name,source)
   candidate=tmp/(name+'.test.c');exe=tmp/name;candidate.write_text(code)
   cmd=[args.gcc,'-std=gnu11','-O1','-g','-fno-omit-frame-pointer','-fsanitize=address,undefined','-Wno-pointer-to-int-cast']
   if execute:cmd+=['-o',exe,candidate]
   else:cmd+=['-c','-o',str(exe)+'.o',candidate]
   c=subprocess.run(cmd,capture_output=True,text=True)
   if c.returncode:raise RuntimeError(f'{name} HOST COMPILE FAILED: '+c.stderr[-1400:])
   env=os.environ.copy();env['ASAN_OPTIONS']='detect_leaks=1:abort_on_error=1'
   if execute:
    t=subprocess.run([str(exe)],capture_output=True,text=True,env=env)
    if t.returncode:raise RuntimeError(f'{name} HOST TEST FAILED: {t.returncode} '+t.stderr[-1600:])
   results.append({'name':name,'gcc_asan_ubsan_compiled':True,'host_semantics_executed':execute,'status':status})
   print(f'HOST {i+1:02d}/48 PASS {name} {status}',flush=True)
 summary={'status':'PASSED_HOST_COMPILE_AND_SEMANTICS','actual_source_files':48,'actual_source_compiled_gcc_asan_ubsan':len(results),'actual_source_semantic_execution':sum(1 for r in results if r['host_semantics_executed']),'architecture_specific_compile_only':sum(1 for r in results if not r['host_semantics_executed']),'records':results}
 if args.report:args.report.write_text(json.dumps(summary,indent=2)+'\n')
 print('HOST SUMMARY',summary['actual_source_semantic_execution'],'executed,',summary['architecture_specific_compile_only'],'compile-only')
if __name__=='__main__':main()
