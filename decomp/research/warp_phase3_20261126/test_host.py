"""Actual-source host call-order test. Not a guest ABI or runtime test."""
import argparse, json, re, subprocess
from pathlib import Path
P=Path(__file__).parent
T=r'''
#include <assert.h>
#include <stdint.h>
#include <string.h>
#include "sources/usa_candidate.c"
static union { long double align; u8 bytes[0x40000]; } sysmem;
u8 *D_8015C5C8_15D1C8=sysmem.bytes;
float D_8020A6DC_5C65EC=0.75f;
Task *D_801FC604_5B8514,*D_801FC638_5B8548;
void *D_801FC60C_5B851C,*D_801FC614_5B8524,*D_801FC61C_5B852C,*D_801FC624_5B8534;
int D_8020C860_5C8770[49]; u8 D_801FC640_5B8550[8]; int D_8015C5DC_15D1DC;
static Task parent, child, root; static int ob, aob, bob, field; static int step; static Pending *p;
void func_801CB7D4_5876E4(void){} void func_801E8EC4_5A4DD4(void){} void func_801CB800_587710(void){}
Task *func_800358E8_364E8(void *a,void (*cb)(void),void *b,void *c,float x,float y,float z,u16 r,u16 s,u16 t,float i,float j,float k,u16 m,u16 n){
 assert(step++==0 && a==&root && cb==func_801CB7D4_5876E4 && !b && !c);
 assert(x==(float)p->x && y==(float)p->y && z==(float)p->z && r==0 && s==p->heading && t==0 && i==D_8020A6DC_5C65EC && j==i && k==i && m==0 && n==0);
 return &parent;
}
void *func_80035EEC_36AEC(Task *a,int b,int c){assert(a==&parent && b==2 && c==1 && (step==1||step==2)); assert(D_801FC604_5B8514==&parent && parent.field5c==D_8020C860_5C8770 && D_8020C860_5C8770[0]==0 && D_8020C860_5C8770[1]==12345 && D_801FC60C_5B851C==&ob);return step++==1?&aob:&bob;}
void func_8001C9BC_1D5BC(void *a,void *b){assert(b==&ob && (step==3||step==4) && a==(step==3?(void*)&aob:(void*)&bob));step++;}
void func_801D9B78_595A88(void *a){assert(step++==5 && a==&bob && parent.field60==(u8)D_8015C5DC_15D1DC);}
void func_801CBC40_587B50(void){assert(step++==6 && parent.field54==D_801FC640_5B8550);}
void func_801D23D4_58E2E4(void){assert(step++==7);}
Task *func_80034E08_35A08(void *a,void (*cb)(void),int b){assert(step++==8 && a==&root && cb==func_801E8EC4_5A4DD4 && b==0 && parent.field64==&field && parent.field90==0);return &child;}
void func_8003521C_35E1C(void (*cb)(void)){assert(step++==9 && cb==func_801CB800_587710 && parent.fielddc==&child && child.field5c==&parent && D_801FC638_5B8548==&child);}
int main(void){
 p=(Pending*)(sysmem.bytes+0x38000);
 for(unsigned i=0;i<4096;i++){
  step=0; memset(&parent,0,sizeof(parent)); memset(&child,0,sizeof(child)); parent.object=&ob; parent.field90=0xff;
  D_801FC624_5B8534=&field; D_8015C5DC_15D1DC=(int)(i*257); D_8020C860_5C8770[0]=1234; D_8020C860_5C8770[1]=12345;
  p->x=(s16)(i*17u);p->y=(s16)(i*37u);p->z=(s16)(i*101u);p->heading=(u16)(i*257u);
  func_801CB5D0_5874E0(&root,0);assert(step==10 && D_801FC614_5B8524==&aob && D_801FC61C_5B852C==&bob);
 }
 return 0;
}
'''
def main():
 a=argparse.ArgumentParser();a.add_argument('--work',type=Path,required=True);args=a.parse_args();args.work.mkdir(parents=True,exist_ok=True)
 m=json.loads((P/'symbol_map.json').read_text());rows=[]
 for r in ['usa','japan_0']:
  s=T if r=='usa' else re.sub(r'\b(?:'+'|'.join(m)+r')\b',lambda x:m[x[0]],T).replace('usa_candidate.c','japan_0_candidate.c')
  p=args.work/f'{r}.c';p.write_text(s);out=args.work/f'{r}.test';cmd=['gcc','-std=c11','-O1','-g','-fsanitize=address,undefined','-fno-sanitize-recover=all','-fno-pie','-no-pie','-I'+str(P),str(p),'-o',str(out)];subprocess.run(cmd,check=True);subprocess.run([out],check=True);rows.append({'region':r,'cases':4096,'sanitizers':'address,undefined','status':'PASS','scope':'synthetic call order/arguments and field relationships, host layout only'});print(r,'4096 cases PASS')
 (args.work/'host.json').write_text(json.dumps(rows,indent=2)+'\n')
if __name__=='__main__':main()
