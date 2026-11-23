/* Host-only behavior regression for the two still-ASM-owned source candidates. */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdalign.h>

alignas(4) unsigned char D_8015CC30_15D830[0xDC];
unsigned char D_8006D920_6E520[8];
void *D_801C7750_1C8350;
int D_801C7740_1C8340,D_801C7754_1C8354,D_801C77E0_1C83E0;
static unsigned char object[0x80];
static int calls,events[4],params[4],expect_spawn;
void func_80218F30_5D4400(void){}
void func_8021925C_5D472C(void){}
void *func_80035690_36290(int a,int b,int c,void *d,float e,float f,float g,int h,int i,int j,float k,float l,float m,int n,int o,int p){
    assert(p==0);
    assert(calls++==0 && a==expect_spawn && b==D_801C7740_1C8340 && c==0 && d==D_8006D920_6E520);
    assert(e==0.0f && f==0.0f && g==0.0f && h==0 && i==0 && j==0 && k==0.1f && l==0.1f && m==0.1f && n==0 && o==0);
    return object;
}
void func_80035244_35E44(void *p,void *callback){assert(calls++==1 && p==object && callback==(void*)func_80218F30_5D4400 && D_801C7750_1C8350==object);}
void func_80035214_35E14(void *p,void *callback){assert(calls++==2 && p==object && callback==(void*)func_8021925C_5D472C && D_801C7750_1C8350==object);}
void func_8003F37C_3FF7C(void);
short *func_8003DF98_3EB98(int,short*);
static void event(int id,int param){assert(calls<4);events[calls]=id;params[calls++]=param;}
#define NOARG(fn,id) void fn(void){event(id,0);}
#define ONEARG(fn,id) void fn(int a){assert(a==D_801C7754_1C8354);event(id,0);}
NOARG(func_8000C3EC_CFEC,1) NOARG(func_8003E1A8_3EDA8,2) NOARG(func_8003E548_3F148,3) NOARG(func_8003E5B8_3F1B8,4)
ONEARG(func_8000D2C0_DEC0,5) ONEARG(func_8000C454_D054,6) ONEARG(func_8000C488_D088,7) ONEARG(func_8000C570_D170,8) ONEARG(func_8000C5A4_D1A4,9) ONEARG(func_8000C60C_D20C,10) ONEARG(func_8000C640_D240,11)
void func_8000C53C_D13C(int a,int b){assert(a==D_801C7754_1C8354);event(12,b);}
void func_8000C430_D030(int a,int b){assert(a==D_801C7754_1C8354);event(13,b);}
void func_8000C568_D168(int a,float b){assert(a==D_801C7754_1C8354 && b==3.0f);event(14,3);}
void func_8000C5E4_D1E4(int a,float b){assert(a==D_801C7754_1C8354 && b==2.0f);event(15,2);}
static void check_dispatch(int op,int unused){
    short script[2]={(short)op,0x1234};calls=0;D_801C77E0_1C83E0=-123;D_801C7754_1C8354=op*17;
    assert(func_8003DF98_3EB98(unused,script)==script+1 && script[0]==op && script[1]==0x1234);
    int n=1,ev=0,param=0,ev2=0,param2=0,state=-123;
    switch(op){
      case -60:ev=1;break;case -61:ev=2;break;case -62:n=0;state=4;break;case -63:ev=5;break;
      case -70:ev=3;break;case -71:ev=4;break;
      case -32:case -33:case -34:case -35:case -36:ev=12;param=(-op-32)*2;break;case -37:ev=12;break;
      case -50:ev=6;break;case -51:ev=7;break;case -52:case -53:ev=13;param=9;break;
      case -54:n=2;ev=8;ev2=14;param2=3;break;case -55:ev=9;break;
      case -56:n=2;ev=15;param=2;ev2=10;break;case -57:ev=11;break;
      default:n=0;break;
    }
    assert(calls==n && D_801C77E0_1C83E0==state);
    if(n>0)assert(events[0]==ev && params[0]==param);
    if(n>1)assert(events[1]==ev2 && params[1]==param2);
}
int main(void){
    for(int k=0;k<4096;k++){
        unsigned char before=(unsigned char)k;expect_spawn=k-2048;memcpy(D_8015CC30_15D830+0x8C,&expect_spawn,4);
        D_8015CC30_15D830[0xD8]=before;D_801C7740_1C8340=k*3;memset(object,0xA5,sizeof(object));D_801C7750_1C8350=0;calls=0;
        func_8003F37C_3FF7C();assert(calls==3 && object[0x74]==before && D_8015CC30_15D830[0xD8]==(unsigned char)(before+1));
        for(int i=0;i<(int)sizeof(object);i++)if(i!=0x74)assert(object[i]==0xA5);
    }
    for(int op=-32768;op<=32767;op++){check_dispatch(op,0);check_dispatch(op,1);}
    puts("F37C: 4096 spawn cases; DF98: 131072 opcode/unused cases PASS");return 0;
}
