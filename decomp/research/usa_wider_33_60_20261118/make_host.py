import json,re
from pathlib import Path
root=Path('/tmp/goemon-beyond-33to60')
rows=json.loads((root/'probe_results.json').read_text())
rows=[r for r in rows if r['status']=='EXACT']
p=[r'#include <assert.h>',r'#include <stdint.h>',r'#include <string.h>',r'#include <stdio.h>',r'',r'#define SUITE_ASSERT(x) assert((x))',r'']
for r in rows:
 name=r['name'];kind=r['kind']
 if kind=='empty0':p.append(f'void {name}(void);')
 elif kind=='divide':p.append(f'int {name}(void*);')
 elif kind=='store_arg1':p.append(f'void {name}(void*,uint32_t);')
 elif kind=='multiply':p.append(f'void {name}(void*,uint32_t);')
 else:p.append(f'void {name}(void*,void*);')
p.append(r'''
static void put_u32(unsigned char *p,uint32_t n){memcpy(p,&n,4);}
static uint32_t get_u32(unsigned char *p){uint32_t n;memcpy(&n,p,4);return n;}
static void put_u16(unsigned char *p,uint16_t n){memcpy(p,&n,2);}
static uint16_t get_u16(unsigned char *p){uint16_t n;memcpy(&n,p,2);return n;}
int main(void){
 _Alignas(16) unsigned char actor[0x180];
 _Alignas(16) unsigned char ctx[0x180];
 unsigned tested=0;
''')
for r in rows:
 name=r['name'];kind=r['kind'];src=r['source']
 if kind=='empty0':
  p.append(f' {name}(); tested++;')
 elif kind=='empty2':
  p.append(f' memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);{name}(actor,ctx);')
  p.append(r' for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;')
 elif kind=='multiply':
  off=int(re.search(r'\+0x([0-9A-F]+)',src).group(1),16);k=int(re.search(r'b\*(\d+)u',src).group(1))
  p.append(f' memset(actor,0,sizeof actor);{name}(actor,7u);SUITE_ASSERT(get_u32(actor+0x{off:X})=={k}u*7u);{name}(actor,0xFFFFFFFFu);SUITE_ASSERT(get_u32(actor+0x{off:X})==(uint32_t)({k}u*0xFFFFFFFFu));tested++;')
 elif kind=='divide':
  off=int(re.search(r'\+0x([0-9A-F]+)',src).group(1),16);k=int(re.search(r'\)/(\d+)',src).group(1))
  p.append(f' put_u32(actor+0x{off:X},(uint32_t)-{k*3+2});SUITE_ASSERT({name}(actor)==-3);put_u32(actor+0x{off:X},{k*5+1}u);SUITE_ASSERT({name}(actor)==5);tested++;')
 elif kind=='store_arg1':
  off=int(re.search(r'\+0x([0-9A-F]+)',src).group(1),16)
  p.append(f' memset(actor,0,sizeof actor);{name}(actor,0xDEADBEEFu);SUITE_ASSERT(get_u32(actor+0x{off:X})==0xDEADBEEFu);tested++;')
 elif kind=='short_decrement':
  off=int(re.search(r'\+0x([0-9A-F]+)',src).group(1),16);k=int(re.search(r'-= (\d+)',src).group(1))
  p.append(f' memset(ctx,0,sizeof ctx);put_u16(ctx+0x{off:X},0);{name}(actor,ctx);SUITE_ASSERT(get_u16(ctx+0x{off:X})==(uint16_t)-{k});put_u16(ctx+0x{off:X},0x7777);{name}(actor,ctx);SUITE_ASSERT(get_u16(ctx+0x{off:X})==(uint16_t)(0x7777u-{k}u));tested++;')
p.append(f' assert(tested=={len(rows)});printf("PASS: %u actual original-address C functions, ASan/UBSan, side effects, bounds, identities\\n",tested);return 0;}}')
(root/'test_native_wide_33_60.c').write_text('\n'.join(p)+'\n')
print('test cases:',len(rows),'bytes:',(root/'test_native_wide_33_60.c').stat().st_size)
