#include <assert.h>
#include "common.h"
void func_8001F878_20478(u16 *,u16 *,u16 *);
void func_8001F914_20514(void); void func_8001FA3C_2063C(void);
static SYS_W sys; SYS_W *D_8015C5C8_15D1C8=&sys;
u16 D_800C7A76_C8676; s32 D_8006D328_6DF28; static int stage;
void func_80020440_21040(void) { assert(stage==0 && D_800C7A76_C8676==9); stage=1; }
void func_80003478_4078(void) { assert(stage==1 && D_800C7A76_C8676==0); stage=2; }
void func_80004240_4E40(void) { assert(stage==2); stage=3; }
void func_80034EF8_35AF8(s32 x) { assert(stage==3 && x==123 && sys.unk_3addf==0); stage=4; }
int main(void) { u16 a=0,b=1,c=1023; func_8001F878_20478(&a,&b,&c); assert(a==512 && b==511 && c==511); a=0; func_8001F878_20478(&a,&a,&a); assert(a==512); D_800C7A76_C8676=9; D_8006D328_6DF28=123; func_8001F914_20514(); assert(stage==2); func_8001FA3C_2063C(); assert(stage==4 && sys.unk_3addf==1); return 0; }
