#include <stdint.h>
#include <assert.h>
#include <stdio.h>
#include "common.h"

TASK_W* D_8016DAB4_16E6B4;
static TASK_W sink;
static TASK_W *a,*b,*result;
static unsigned short mask;
static int function_index;
static int calls[3];
static int total;
static void cb(TASK_W *p, struct CLS_W *q) {(void)p;(void)q;}
TASK_W *func_80034B24_35724(TASK_W *arg,unsigned short bits){a=arg;mask=bits;calls[total++]=1;return result;}
TASK_W *func_80034B58_35758(TASK_W *root,TASK_W *arg,unsigned short bits){a=root;b=arg;mask=bits;calls[total++]=2;return result;}
TASK_W *func_80034C4C_3584C(TASK_W *arg,unsigned short bits){a=arg;mask=bits;calls[total++]=3;return result;}
TASK_W *func_80034C84_35884(TASK_W *arg,unsigned short bits){a=arg;mask=bits;calls[total++]=4;return result;}
void func_80034D24_35924(TASK_W *arg){assert(arg==result);calls[total++]=5;function_index++;}
void func_80035204_35E04(void (*ptr)(TASK_W*,struct CLS_W*));
void func_80035214_35E14(TASK_W*,void (*ptr)(TASK_W*,struct CLS_W*));
void func_80034DD8_359D8(TASK_W*,unsigned short);
void func_80034E08_35A08(TASK_W*,TASK_W*,unsigned short);
void func_80034E38_35A38(TASK_W*,unsigned short);
void func_80034E68_35A68(TASK_W*,unsigned short);
static void reset(void) {a=b=0;mask=0;total=0;calls[0]=calls[1]=calls[2]=0;}
int main(void) {
 TASK_W x={0},y={0};
 D_8016DAB4_16E6B4=&x;
 func_80035204_35E04(cb);assert(x.exec[0]==cb);
 func_80035214_35E14(&y,cb);assert(y.exec[0]==cb);
 result=&sink;
 for (int i=0;i<256;i++) {
   unsigned short bits=(unsigned short)((unsigned)i*257u);
   reset();func_80034DD8_359D8(&x,bits);assert(a==&x&&mask==bits&&total==2&&calls[0]==1&&calls[1]==5);
   reset();func_80034E08_35A08(&x,&y,bits);assert(a==&x&&b==&y&&mask==bits&&total==2&&calls[0]==2&&calls[1]==5);
   reset();func_80034E38_35A38(&x,bits);assert(a==&x&&mask==bits&&total==2&&calls[0]==3&&calls[1]==5);
   reset();func_80034E68_35A68(&x,bits);assert(a==&x&&mask==bits&&total==2&&calls[0]==4&&calls[1]==5);
 }
 assert(function_index==1024);
 puts("PASS: 2 callback setters; 4 wrappers x 256 cases (1024 call chains)");
 return 0;
}
