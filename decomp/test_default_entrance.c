#include <assert.h>
#include <stddef.h>
#include "default_entrance.h"
static SYS_W sys; SYS_W *D_8015C5C8_15D1C8=&sys;
SaveData D_8015C608_15D208; Entry D_8006B780_6C380[3];
s32 D_8006CFBC_6DBBC, D_8006CFB8_6DBB8, D_8015C5DC_15D1DC;
static int stage;
void func_8000B864_C464(void) { assert(stage==0); assert(sys.unk_cf8a0==1 && D_8015C608_15D208.half_204==1 && D_8015C608_15D208.byte_206==7 && D_8015C5DC_15D1DC==99 && D_8015C608_15D208.half_20A==-10); stage=1; }
void func_80003728_4328(u8 x) { assert(x==0x0B); if (D_8006CFBC_6DBBC==0xFF) assert(stage==2); else assert(stage==1); stage++; }
void func_80021444_22044(void);
int main(void) {
 _Static_assert(offsetof(SYS_W,intended_room_id)==0x3ADF2,"room offset"); _Static_assert(sizeof(Entry)==10,"record size");
 sys.intended_room_id=1; D_8006B780_6C380[1]=(Entry){-10,20,-30,1023,7};
 D_8015C608_15D208.byte_207=0x5a; func_800214E4_220E4();
 assert(D_8015C608_15D208.half_20A==-10 && D_8015C608_15D208.half_20C==20 && D_8015C608_15D208.half_20E==-30);
 assert(D_8015C608_15D208.half_210==1023 && D_8015C608_15D208.half_208==7 && D_8015C608_15D208.byte_207==0x5a);
 sys.intended_room_id=2; D_8006B780_6C380[2]=(Entry){0,0,0,8,9}; func_800214E4_220E4();
 assert(D_8015C608_15D208.half_20A==0 && D_8015C608_15D208.half_20C==0 && D_8015C608_15D208.half_20E==0 && D_8015C608_15D208.half_210==0 && D_8015C608_15D208.half_208==0 && D_8015C608_15D208.byte_207==0x5a);
 D_8006CFBC_6DBBC=0; D_8006CFB8_6DBB8=99; sys.intended_room_id=1; sys.intended_room_group=7; func_80021444_22044(); assert(stage==2);
 D_8006CFBC_6DBBC=0xFF; sys.unk_cf8a0=0; D_8015C608_15D208.half_204=42; func_80021444_22044(); assert(stage==3 && sys.unk_cf8a0==0 && D_8015C608_15D208.half_204==42);
 return 0;
}
