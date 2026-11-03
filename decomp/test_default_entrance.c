#include <assert.h>
#include <stddef.h>
#include "default_entrance.h"
static SYS_W sys; SYS_W *D_8015C5C8_15D1C8=&sys;
SaveData D_8015C608_15D208; Entry D_8006B780_6C380[3];
int main(void) {
 _Static_assert(offsetof(SYS_W,intended_room_id)==0x3ADF2,"room offset"); _Static_assert(sizeof(Entry)==10,"record size");
 sys.intended_room_id=1; D_8006B780_6C380[1]=(Entry){-10,20,-30,1023,7};
 D_8015C608_15D208.byte_207=0x5a; func_800214E4_220E4();
 assert(D_8015C608_15D208.half_20A==-10 && D_8015C608_15D208.half_20C==20 && D_8015C608_15D208.half_20E==-30);
 assert(D_8015C608_15D208.half_210==1023 && D_8015C608_15D208.half_208==7 && D_8015C608_15D208.byte_207==0x5a);
 sys.intended_room_id=2; D_8006B780_6C380[2]=(Entry){0,0,0,8,9}; func_800214E4_220E4();
 assert(D_8015C608_15D208.half_20A==0 && D_8015C608_15D208.half_20C==0 && D_8015C608_15D208.half_20E==0 && D_8015C608_15D208.half_210==0 && D_8015C608_15D208.half_208==0 && D_8015C608_15D208.byte_207==0x5a);
 return 0;
}
