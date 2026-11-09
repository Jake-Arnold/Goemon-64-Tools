/* Synthetic mock-game regression for the research-only VM loader. */
#include <assert.h>
#include <stddef.h>
#include <stdint.h>
#include <string.h>
#define GOEMON_DECOMP_HOST_TEST 1
#include "candidates/vm_loader_storage_probe.c"
void *D_80077860_78460;
s32 D_8007785C_7845C, D_80077858_78458;
VmResource D_801C78E8_1C84E8;
VmWorkLoader D_801C77E8_1C83E8;
s32 D_801C7900_1C8500,D_801C7904_1C8504;
s32 D_801C7740_1C8340,D_801C7744_1C8344,D_801C7748_1C8348,D_801C774C_1C834C;
s32 D_801C7750_1C8350,D_801C7754_1C8354,D_801C7758_1C8358,D_801C775C_1C835C;
s32 D_801C7760_1C8360,D_801C7764_1C8364,D_801C7768_1C8368,D_801C776C_1C836C;
s32 D_801C7770_1C8370,D_801C7774_1C8374,D_801C7798_1C8398,D_801C77A0_1C83A0;
s32 D_801C77D8_1C83D8,D_801C77E0_1C83E0;
s32 D_801C78D0_1C84D0,D_801C78FC_1C84FC;
s32 D_801C7920_1C8520,D_801C7924_1C8524,D_801C7928_1C8528,D_801C792C_1C852C;
_Static_assert(offsetof(VmWorkLoader, marker)==8, "VM marker offset");
_Static_assert(offsetof(VmWorkLoader, gate)==10, "VM gate offset");
_Static_assert(offsetof(VmWorkLoader, loaded)==20, "VM load offset");
_Static_assert(offsetof(VmResource, unk4)==4, "Resource +4 offset");
static int load_calls, restore_calls, reset_calls, size_calls, delta_calls, init_calls, retry;
static s32 final_return, init_arg, delta_arg;
static u16 recovered_halfword;
s32 func_800141C4_14DC4(s32 resource) {assert(resource == D_801C78E8_1C84E8.id.word);load_calls++;return retry && load_calls==1 ? -1 : final_return;}
void func_80013B14_14714(u16 id){restore_calls++;recovered_halfword=id;}
void func_8003CFA0_3DBA0(s32 resource){assert(resource == D_801C78E8_1C84E8.id.word);reset_calls++;}
s32 func_80001E50_2A50(s32 resource){assert(resource == D_801C78E8_1C84E8.id.word);size_calls++;return resource ^ 0x31415;}
s32 func_8003DDC4_3E9C4(s32 start,s32 resource){assert(resource==D_801C78E8_1C84E8.id.word);delta_calls++;delta_arg=start;return start+0x2a;}
s32 func_8003DE48_3EA48(s32 start){init_calls++;init_arg=start;return start+123;}
void func_80024088_24C88(s32 code){assert(code==0x82);}
static void reset_mocks(void){ load_calls=restore_calls=reset_calls=size_calls=delta_calls=init_calls=0;retry=0;final_return=0;init_arg=delta_arg=0;recovered_halfword=0;}
static void check_common(void){
 assert(D_801C7740_1C8340==0 && D_801C7754_1C8354==0);
 assert(D_801C7758_1C8358==24 && D_801C775C_1C835C==24 && D_801C7760_1C8360==24 && D_801C7764_1C8364==24);
 assert(D_801C7770_1C8370==0 && D_801C7774_1C8374==0 && D_801C7798_1C8398==1);
 assert(D_801C77D8_1C83D8==1 && D_801C77E0_1C83E0==0);
 assert(D_801C77E8_1C83E8.value==0 && D_801C77E8_1C83E8.marker==-1 && D_801C77E8_1C83E8.gate==0 && D_801C77E8_1C83E8.unkC==0);
 assert(D_801C78D0_1C84D0==0 && D_801C7920_1C8520==0 && D_801C792C_1C852C==0);
 assert(D_8007785C_7845C==256);
}
int main(void){
 u8 owner[0x60];
 for(int i=1;i<=100;i++){
  const s32 resource_id = (s32)(((u32)(0x1200+i)<<16) | (u32)(0x5600+(i%13)));
  memset(owner,0x55,sizeof(owner));reset_mocks();D_80077860_78460=0;
  D_801C78E8_1C84E8.id.word=0x12345;D_801C77E8_1C83E8.loaded=123456;
  assert(func_8003D468_3E068(i,i)==0);assert(D_801C77E8_1C83E8.loaded==123456);assert(load_calls==0 && init_calls==0);
  reset_mocks();D_80077860_78460=owner;final_return=(s32)0xC0003400u;
  assert(func_8003D468_3E068(i,resource_id)==1);
  assert(D_801C77E8_1C83E8.loaded==(s32)0x80003400u);
  assert(D_801C78E8_1C84E8.unk4==(resource_id^0x31415) && D_801C78E8_1C84E8.unk8==0x2a);
  assert(D_80077858_78458==i+123 && init_arg==i && delta_arg==i);
  assert(load_calls==1 && restore_calls==0 && reset_calls==0 && size_calls==1 && delta_calls==1 && init_calls==1);
  assert(owner[0x5c]==0 && owner[0x5d]==0);check_common();
  reset_mocks();memset(owner,0x55,sizeof(owner));final_return=(s32)0xC0004500u;retry=1;
  assert(func_8003D468_3E068(i,resource_id)==1);
  assert(load_calls==2 && restore_calls==1 && reset_calls==1);
  assert(recovered_halfword==(u16)resource_id);
#if defined(__BYTE_ORDER__) && defined(__ORDER_LITTLE_ENDIAN__) && (__BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__)
  assert(D_801C78E8_1C84E8.id.half.lower != (u16)resource_id); /* Host-only negative control. */
#endif
  assert(D_801C77E8_1C83E8.loaded==(s32)0x80004500u);check_common();
  reset_mocks();memset(owner,0x55,sizeof(owner));
  D_801C7900_1C8500=0;D_801C7904_1C8504=0;
  assert(func_8003D468_3E068(i,-1)==1);
  assert(D_801C77E8_1C83E8.loaded==0 && D_801C78E8_1C84E8.unk4==0 && D_801C78E8_1C84E8.unk8==0);
  assert(D_801C7900_1C8500==3 && D_801C7904_1C8504==-1 && D_80077858_78458==0);
  assert(load_calls==0 && restore_calls==0 && init_calls==0 && size_calls==0);check_common();
 }
 return 0;
}
